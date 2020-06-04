from flask import Flask
from flask_restx import Api, Resource, reqparse, fields, abort

from bank_api.bank import Bank
from bank_api.bank_reporter import BankReporter


def create_app():
    # Set up framework and service classes
    app = Flask(__name__)
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    api = Api(app, title='My Banking API',
            description='A simple banking API for learning Test-Driven-Development')
    bank = Bank()
    bank_reporter = BankReporter(bank)

    # Custom API documentation
    add_money = api.model("Add", {
        'name': fields.String,
        'amount': fields.Integer
    })

    move_money = api.model("Move", {
        'name_from': fields.String,
        'name_to': fields.String,
        'amount': fields.Integer
    })


    @api.route('/accounts/<string:name>')
    class AccountResource(Resource):
        def post(self, name):
            """Create a new named Account"""
            try:
                return bank.create_account(name).to_dict()
            except Exception as e:
                abort(400, str(e))

        def get(self, name):
            """Get an Account"""
            try:
                account = bank.get_account(name).to_dict()
                account['balance'] = bank_reporter.get_balance(account['name'])
                return account
            except Exception:
                abort(404, 'Account not found')


    @api.route('/money')
    class AddMoneyResource(Resource):
        @api.expect(add_money)
        def post(self):
            """Add funds to an account"""
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='Account name')
            parser.add_argument('amount', type=int, help='Transfer amount (pence)')
            args = parser.parse_args()
            return bank.add_funds(**args)


    @api.route('/money/move')
    class MoveMoneyResource(Resource):
        @api.expect(move_money)
        def post(self):
            """Move funds between accounts"""
            parser = reqparse.RequestParser()
            parser.add_argument('name_from', type=str, help='Account name (from)')
            parser.add_argument('name_to', type=str, help='Account name (to)')
            parser.add_argument('amount', type=int, help='Transfer amount (pence)')
            args = parser.parse_args()
            return bank.move_funds(**args)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
