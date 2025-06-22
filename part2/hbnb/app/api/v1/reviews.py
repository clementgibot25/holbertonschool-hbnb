from flask_restx import Namespace, Resource, fields, abort
from http import HTTPStatus
from app.services.facade import hbnb_facade as facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(
        required=True,
        description='Text of the review',
        example='The place was great!',
        min_length=1,
        max_length=1000,
        pattern=r"^[a-zA-Zà-ÿÀ-Ÿ\s\-']+$",),
    'rating': fields.Integer(required=True,
        description='Rating of the place (1-5)',
        example=5,
        min=1,
        max=5),
    'user_id': fields.String(required=True,
        description='ID of the user',
        example='user_12345'),
    'place_id': fields.String(required=True,
        description='ID of the place',
        example='place_12345')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    def post(self):
        """Register a new review"""
        try:
            review_data = api.payload
            new_review = facade.create_review(
                text=review_data['text'],
                rating=review_data['rating'],
                user_id=review_data['user_id'],
                place_id=review_data['place_id']
            )
            if not new_review:
                abort(HTTPStatus.BAD_REQUEST, 'Invalid input data')
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id
            }, HTTPStatus.CREATED
        except Exception as e:
            # Les erreurs de validation sont déjà gérées par le service
            # On laisse passer l'exception pour qu'elle soit traitée par le gestionnaire d'erreurs de Flask-RestX
            raise

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [{'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user_id, 'place_id': review.place_id} for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user_id, 'place_id': review.place_id}, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review, User or Place not found')
    def put(self, review_id):
        """Update a review's information"""
        try:
            review_data = api.payload
            updated_review = facade.update_review(review_id, **review_data)
            if not updated_review:
                abort(HTTPStatus.NOT_FOUND, 'Review not found')
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id
            }, HTTPStatus.OK
        except Exception as e:
            # Les erreurs de validation sont déjà gérées par le service
            # On laisse passer l'exception pour qu'elle soit traitée par le gestionnaire d'erreurs de Flask-RestX
            raise

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        if not facade.get_review(review_id):
            abort(HTTPStatus.NOT_FOUND, 'Review not found')
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, HTTPStatus.OK

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'Place not found'}, 404
        return [{'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user_id, 'place_id': review.place_id} for review in reviews], 200
