from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from model import db, User, Tweet, Follow, Favorite
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.config['SECRET_KEY'] = os.environ.get(
    'SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitter_clone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def init_db():
    with app.app_context():
        db.create_all()


def login_required(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    if 'user_id' in session:
        return db.session.get(User, session['user_id'])
    return None


@app.route('/')
def index():
    trends = Tweet.query.join(Favorite).group_by(
        Tweet.id).having(
        db.func.count(
            Favorite.id) >= 2).order_by(
                db.func.count(
                    Favorite.id).desc()).limit(100).all()
    current_user = get_current_user()
    return render_template(
        'trend.html',
        tweets=trends,
        current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mailaddress = request.form['mailaddress']
        password = request.form['password']

        user = User.query.filter_by(mailaddress=mailaddress).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('timeline'))
        else:
            flash('Email address or password is incorrect')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mailaddress = request.form['mailaddress']
        password = request.form['password']

        if User.query.filter_by(mailaddress=mailaddress).first():
            flash('This email address is already registered')
            return render_template('login.html')

        user = User(name=name, mailaddress=mailaddress)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return redirect(url_for('timeline'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/timeline')
@login_required
def timeline():
    current_user = get_current_user()
    following_ids = [f.following_id for f in current_user.following.all()]

    tweets = Tweet.query.filter(
        Tweet.user_id.in_(following_ids)).order_by(
        Tweet.created_at.desc()).limit(100).all()
    return render_template(
        'timeline.html',
        tweets=tweets,
        current_user=current_user)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    if request.method == 'POST':
        msg = request.form['msg']

        if not msg or len(msg) > 128:
            flash('Tweet must be between 1 and 128 characters')
            return render_template(
                'post.html', current_user=get_current_user())

        tweet = Tweet(user_id=session['user_id'], msg=msg)
        db.session.add(tweet)
        db.session.commit()

        return redirect(url_for('timeline'))

    return render_template('post.html', current_user=get_current_user())


@app.route('/tweet', methods=['POST'])
@login_required
def tweet():
    msg = request.form['msg']

    if not msg or len(msg) > 128:
        return jsonify({'error': 'Tweet must be between 1 and 128 characters'}), 400

    tweet = Tweet(user_id=session['user_id'], msg=msg)
    db.session.add(tweet)
    db.session.commit()

    return jsonify({'success': True})


@app.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow_user(user_id):
    current_user = get_current_user()
    user_to_follow = db.get_or_404(User, user_id)

    if current_user.id == user_id:
        return jsonify({'error': 'You cannot follow yourself'}), 400

    current_user.follow(user_to_follow)
    db.session.commit()

    return jsonify({'success': True})


@app.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow_user(user_id):
    current_user = get_current_user()
    user_to_unfollow = db.get_or_404(User, user_id)

    current_user.unfollow(user_to_unfollow)
    db.session.commit()

    return jsonify({'success': True})


@app.route('/favorite/<int:tweet_id>', methods=['POST'])
@login_required
def favorite_tweet(tweet_id):
    current_user = get_current_user()
    tweet = db.get_or_404(Tweet, tweet_id)

    current_user.favorite(tweet)
    db.session.commit()

    return jsonify({'success': True})


@app.route('/unfavorite/<int:tweet_id>', methods=['POST'])
@login_required
def unfavorite_tweet(tweet_id):
    current_user = get_current_user()
    tweet = db.get_or_404(Tweet, tweet_id)

    current_user.unfavorite(tweet)
    db.session.commit()

    return jsonify({'success': True})


@app.route('/favorites')
@login_required
def favorites():
    current_user = get_current_user()
    favorite_tweets = Tweet.query.join(Favorite).filter(
        Favorite.user_id == current_user.id).order_by(
        Favorite.created_at.desc()).all()
    return render_template(
        'favorites.html',
        tweets=favorite_tweets,
        current_user=current_user)


@app.route('/followers')
@login_required
def followers():
    current_user = get_current_user()
    follower_users = User.query.join(
        Follow, User.id == Follow.follower_id).filter(
        Follow.following_id == current_user.id).all()
    return render_template(
        'followers.html',
        users=follower_users,
        current_user=current_user)


@app.route('/following')
@login_required
def following():
    current_user = get_current_user()
    following_users = User.query.join(
        Follow, User.id == Follow.following_id).filter(
        Follow.follower_id == current_user.id).all()
    return render_template(
        'following.html',
        users=following_users,
        current_user=current_user)


@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    current_user = get_current_user()

    if not query:
        return render_template(
            'search.html',
            tweets=[],
            query='',
            current_user=current_user)

    tweets = Tweet.query.filter(
        Tweet.msg.contains(query)
    ).order_by(Tweet.created_at.desc()).limit(100).all()

    return render_template(
        'search.html',
        tweets=tweets,
        query=query,
        current_user=current_user)


@app.route('/user/<int:user_id>')
@login_required
def user_profile(user_id):
    user = db.get_or_404(User, user_id)
    current_user = get_current_user()

    # User's tweet list (latest first)
    tweets = Tweet.query.filter_by(
        user_id=user_id).order_by(
        Tweet.created_at.desc()).limit(100).all()

    return render_template(
        'user_profile.html',
        user=user,
        tweets=tweets,
        current_user=current_user)


@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())


# if __name__ == '__main__':
#     init_db()
#     app.run(host='0.0.0.0', port=5000, debug=True)
