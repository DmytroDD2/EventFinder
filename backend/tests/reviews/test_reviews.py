from app.reviews.models import Review
from  ..utils import test_user, test_events, test_events_images, test_events_reviews, test_user_reviews





def test_create_review(client, test_events_images):
    review_data = {
        "rating": 5,
        "description": "string"
        }


    response = client.post(
        f"/reviews/event/{test_events_images.id}/create-review",
        headers={"Authorization": "Bearer valid_token"},
        json=review_data

    )
    assert response.status_code == 201
    data = response.json()
    assert data["rating"] == review_data["rating"]
    assert data["description"] == review_data["description"]


def test_get_all_review(client, test_events_reviews):
    response = client.get(
        f"/reviews/event/{1}?page=1&per_page=10",
        headers={"Authorization": "Bearer valid_token"},
    )
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0

    review = data[0]
    assert review["rating"] == 5
    assert review["description"] == "good event"
    assert review["name"] == "j"
    assert "id" in review
    assert "rating" in review
    assert "description" in review
    assert "user_id" in review
    assert "event_id" in review
    assert "image_url" in review
    assert "name" in review




def test_get_my_review(client, test_user_reviews):
    response = client.get(
        "/reviews/my",
        headers={"Authorization": "Bearer valid_token"},
    )
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    assert "rating" in data[0]
    assert "description" in data[0]
    assert "event_id" in data[0]
    assert "user_id" in data[0]


def test_delete_review(admin, test_events_reviews):
    response = admin.delete(
        f"/reviews/1/delete",
        headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 204


