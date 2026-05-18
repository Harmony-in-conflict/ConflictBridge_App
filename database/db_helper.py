import base64
import hashlib
import hmac
import secrets

import psycopg2

from database.db_connect import DBConnection


PASSWORD_ALGORITHM = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 260_000


def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS
    )
    return "$".join(
        (
            PASSWORD_ALGORITHM,
            str(PASSWORD_ITERATIONS),
            base64.b64encode(salt).decode("ascii"),
            base64.b64encode(digest).decode("ascii"),
        )
    )


def verify_password(password, stored_hash):
    if not stored_hash:
        return False

    # Backward compatibility if a teammate followed the original plan literally.
    if "$" not in stored_hash:
        plain_sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return hmac.compare_digest(plain_sha, stored_hash)

    try:
        algorithm, iterations, salt_b64, digest_b64 = stored_hash.split("$", 3)
        if algorithm != PASSWORD_ALGORITHM:
            return False
        salt = base64.b64decode(salt_b64.encode("ascii"))
        expected = base64.b64decode(digest_b64.encode("ascii"))
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, int(iterations)
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def create_user(username, email, password, country, bio="", avatar_path=None):
    sql = """
        INSERT INTO users (username, email, password_hash, country, bio, avatar_path)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING user_id, username, email, country, bio, avatar_path, created_at;
    """
    try:
        with DBConnection.cursor(commit=True) as cur:
            cur.execute(
                sql,
                (
                    username.strip(),
                    email.strip().lower(),
                    hash_password(password),
                    country.strip() if country else None,
                    bio.strip() if bio else "",
                    avatar_path,
                ),
            )
            return cur.fetchone()
    except psycopg2.IntegrityError as exc:
        raise ValueError("Username or email already exists.") from exc


def authenticate_user(email, password):
    with DBConnection.cursor() as cur:
        cur.execute(
            """
            SELECT user_id, username, email, password_hash, country, bio, avatar_path
            FROM users
            WHERE email = %s;
            """,
            (email.strip().lower(),),
        )
        user = cur.fetchone()
    if user and verify_password(password, user["password_hash"]):
        user.pop("password_hash", None)
        return user
    return None


def get_user(user_id):
    with DBConnection.cursor() as cur:
        cur.execute(
            """
            SELECT user_id, username, email, country, bio, avatar_path, created_at
            FROM users
            WHERE user_id = %s;
            """,
            (user_id,),
        )
        return cur.fetchone()


def update_profile(user_id, country, bio, avatar_path):
    with DBConnection.cursor(commit=True) as cur:
        cur.execute(
            """
            UPDATE users
            SET country = %s, bio = %s, avatar_path = %s
            WHERE user_id = %s
            RETURNING user_id, username, email, country, bio, avatar_path, created_at;
            """,
            (
                country.strip() if country else None,
                bio.strip() if bio else "",
                avatar_path,
                user_id,
            ),
        )
        return cur.fetchone()


def create_post(user_id, title, category, content, country, image_path=None):
    with DBConnection.cursor(commit=True) as cur:
        cur.execute(
            """
            INSERT INTO posts (user_id, title, content, category, image_path, country)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING post_id;
            """,
            (
                user_id,
                title.strip(),
                content.strip(),
                category,
                image_path,
                country.strip() if country else None,
            ),
        )
        return cur.fetchone()["post_id"]


def update_post(post_id, user_id, title, category, content, country, image_path):
    with DBConnection.cursor(commit=True) as cur:
        cur.execute(
            """
            UPDATE posts
            SET title = %s,
                category = %s,
                content = %s,
                country = %s,
                image_path = %s
            WHERE post_id = %s AND user_id = %s
            RETURNING post_id;
            """,
            (
                title.strip(),
                category,
                content.strip(),
                country.strip() if country else None,
                image_path,
                post_id,
                user_id,
            ),
        )
        row = cur.fetchone()
        return row is not None


def delete_post(post_id, user_id):
    with DBConnection.cursor(commit=True) as cur:
        cur.execute(
            """
            DELETE FROM posts
            WHERE post_id = %s AND user_id = %s
            RETURNING post_id;
            """,
            (post_id, user_id),
        )
        return cur.fetchone() is not None


def list_posts(category=None, search=None, country=None, limit=100):
    filters = []
    params = []

    if category and category != "All":
        filters.append("p.category = %s")
        params.append(category)

    if country and country != "All":
        filters.append("p.country = %s")
        params.append(country)

    if search:
        term = f"%{search.strip()}%"
        filters.append(
            "(p.title ILIKE %s OR p.content ILIKE %s OR p.country ILIKE %s OR u.username ILIKE %s)"
        )
        params.extend((term, term, term, term))

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""
    params.append(limit)

    with DBConnection.cursor() as cur:
        cur.execute(
            f"""
            SELECT
                p.post_id,
                p.user_id,
                p.title,
                p.content,
                p.category,
                p.image_path,
                p.country,
                p.created_at,
                u.username,
                COALESCE(COUNT(c.comment_id), 0) AS comment_count,
                COALESCE(SUM(CASE WHEN c.flagged THEN 1 ELSE 0 END), 0) AS flagged_count
            FROM posts p
            JOIN users u ON u.user_id = p.user_id
            LEFT JOIN comments c ON c.post_id = p.post_id
            {where_clause}
            GROUP BY p.post_id, u.username
            ORDER BY p.created_at DESC
            LIMIT %s;
            """,
            tuple(params),
        )
        return cur.fetchall()


def get_post(post_id):
    with DBConnection.cursor() as cur:
        cur.execute(
            """
            SELECT
                p.post_id,
                p.user_id,
                p.title,
                p.content,
                p.category,
                p.image_path,
                p.country,
                p.created_at,
                u.username,
                u.avatar_path,
                COALESCE(COUNT(c.comment_id), 0) AS comment_count
            FROM posts p
            JOIN users u ON u.user_id = p.user_id
            LEFT JOIN comments c ON c.post_id = p.post_id
            WHERE p.post_id = %s
            GROUP BY p.post_id, u.username, u.avatar_path;
            """,
            (post_id,),
        )
        return cur.fetchone()


def list_countries():
    with DBConnection.cursor() as cur:
        cur.execute(
            """
            SELECT country,
                   SUM(post_count)::int AS post_count,
                   SUM(user_count)::int AS user_count
            FROM (
                SELECT country, COUNT(*) AS post_count, 0 AS user_count
                FROM posts
                WHERE country IS NOT NULL AND country <> ''
                GROUP BY country
                UNION ALL
                SELECT country, 0 AS post_count, COUNT(*) AS user_count
                FROM users
                WHERE country IS NOT NULL AND country <> ''
                GROUP BY country
            ) culture_sources
            GROUP BY country
            ORDER BY country ASC;
            """
        )
        return cur.fetchall()


def add_comment(post_id, user_id, content):
    with DBConnection.cursor(commit=True) as cur:
        cur.execute(
            """
            INSERT INTO comments (post_id, user_id, content)
            VALUES (%s, %s, %s)
            RETURNING comment_id;
            """,
            (post_id, user_id, content.strip()),
        )
        return cur.fetchone()["comment_id"]


def list_comments(post_id):
    with DBConnection.cursor() as cur:
        cur.execute(
            """
            SELECT c.comment_id,
                   c.post_id,
                   c.user_id,
                   c.content,
                   c.flagged,
                   c.created_at,
                   u.username
            FROM comments c
            JOIN users u ON u.user_id = c.user_id
            WHERE c.post_id = %s
            ORDER BY c.created_at ASC;
            """,
            (post_id,),
        )
        return cur.fetchall()


def flag_comment(comment_id):
    with DBConnection.cursor(commit=True) as cur:
        cur.execute(
            """
            UPDATE comments
            SET flagged = TRUE
            WHERE comment_id = %s
            RETURNING comment_id;
            """,
            (comment_id,),
        )
        return cur.fetchone() is not None


def list_quiz_countries():
    with DBConnection.cursor() as cur:
        cur.execute(
            """
            SELECT DISTINCT country
            FROM quiz_questions
            ORDER BY country ASC;
            """
        )
        return [row["country"] for row in cur.fetchall()]


def get_random_questions(country, limit=5):
    with DBConnection.cursor() as cur:
        cur.execute(
            """
            SELECT q_id, country, question, option_a, option_b, option_c, option_d,
                   correct_option, explanation
            FROM quiz_questions
            WHERE country = %s
            ORDER BY RANDOM()
            LIMIT %s;
            """,
            (country, limit),
        )
        return cur.fetchall()


def save_quiz_score(user_id, country, score, total_questions):
    percentage = round((score / total_questions) * 100) if total_questions else 0
    with DBConnection.cursor(commit=True) as cur:
        cur.execute(
            """
            INSERT INTO quiz_scores (user_id, country, score, total_questions, percentage)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING score_id;
            """,
            (user_id, country, score, total_questions, percentage),
        )
        return cur.fetchone()["score_id"]


def get_score_history(user_id, limit=10):
    with DBConnection.cursor() as cur:
        cur.execute(
            """
            SELECT score_id, country, score, total_questions, percentage, attempted_at
            FROM quiz_scores
            WHERE user_id = %s
            ORDER BY attempted_at DESC
            LIMIT %s;
            """,
            (user_id, limit),
        )
        return cur.fetchall()


def get_user_comments(user_id, limit=20):
    with DBConnection.cursor() as cur:
        cur.execute(
            """
            SELECT c.comment_id,
                   c.content,
                   c.flagged,
                   c.created_at,
                   p.post_id,
                   p.title AS post_title
            FROM comments c
            JOIN posts p ON p.post_id = c.post_id
            WHERE c.user_id = %s
            ORDER BY c.created_at DESC
            LIMIT %s;
            """,
            (user_id, limit),
        )
        return cur.fetchall()

