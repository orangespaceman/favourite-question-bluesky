import os
import psycopg2
from atproto import Client
from dotenv import load_dotenv

load_dotenv()


class FavouriteQuestion:
    def __init__(self):
        self.db_config = {
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT", "5432"),
        }
        self.connection = None

    def connect(self):
        """Connect to the database"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")

    def close_connection(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

    def get_random_question(self):
        """Fetch a random question that hasn't been posted"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, question
                    FROM questions
                    WHERE date_posted IS NULL
                    ORDER BY RANDOM()
                    LIMIT 1;
                """)
                result = cursor.fetchone()  # (id, question) tuple or None
                return result
        except psycopg2.Error as e:
            print(f"Error fetching random question: {e}")
            return None

    def mark_question_as_posted(self, question_id):
        """Update the question as posted on the current date"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE questions
                    SET date_posted = CURRENT_DATE
                    WHERE id = %s;
                """,
                    (question_id,),
                )
            self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error updating question: {e}")

    def post_to_bluesky(self, question_text):
        try:
            client = Client()
            client.login(os.getenv("BLUESKY_HANDLE"), os.getenv("BLUESKY_PASSWORD"))
            client.send_post(question_text, langs=["en-GB"])
        except Exception as e:
            print(f"Error posting question: {e}")

    def post_question(self):
        """Select a random question, post it, and mark it as posted"""
        question = self.get_random_question()
        if question:
            question_id, question_text = question

            self.post_to_bluesky(question_text)

            self.mark_question_as_posted(question_id)
        else:
            print("No unposted questions found")


def main():
    question = FavouriteQuestion()
    question.connect()
    question.post_question()
    question.close_connection()


if __name__ == "__main__":
    main()
