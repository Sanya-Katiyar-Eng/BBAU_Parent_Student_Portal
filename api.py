from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database.db import get_connection

app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FCMTokenData(BaseModel):
    parent_id: int
    fcm_token: str


@app.post("/save-fcm-token")
def save_fcm_token(data: FCMTokenData):

    conn = get_connection()
    cur = conn.cursor()

    try:

        query = """
            INSERT INTO fcm_tokens
                (parent_id, fcm_token)
            VALUES
                (%s, %s)

            ON CONFLICT (fcm_token)
            DO UPDATE SET
                parent_id = EXCLUDED.parent_id,
                updated_at = CURRENT_TIMESTAMP
        """

        cur.execute(
            query,
            (
                data.parent_id,
                data.fcm_token
            )
        )

        conn.commit()

        return {
            "success": True,
            "message": "FCM token saved successfully"
        }

    except Exception as e:

        conn.rollback()

        print("FCM DATABASE ERROR:", e)

        return {
            "success": False,
            "message": str(e)
        }

    finally:

        cur.close()
        conn.close()