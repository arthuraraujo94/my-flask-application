# app.py

import os

import boto3

from flask import Flask, jsonify, request
app = Flask(__name__)

MATCHES_TABLE = os.environ['MATCHES_TABLE']
client = boto3.client('dynamodb')


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/matches/<string:match_id>")
def get_user(match_id):
    resp = client.get_item(
        TableName=MATCHES_TABLE,
        Key={
            'matchId': { 'S': match_id }
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'User does not exist'}), 404

    return jsonify({
        'matchId': item.get('matchId').get('S'),
        'title': item.get('title').get('S'),
        'matchId': item.get('matchId').get('S'),
        'title': item.get('title').get('S'),
        'home': item.get('home').get('S'),
        'away': item.get('away').get('S'),
        'home_score': item.get('home_score').get('S'),
        'away_score': item.get('away_score').get('S'),
        'description': item.get('description').get('S')
    })


@app.route("/matches", methods=["POST"])
def create_match():
    match_id = request.json.get('matchId')
    title = request.json.get('title')
    home = request.json.get('home')
    away = request.json.get('away')
    home_score = request.json.get('home_score')
    away_score = request.json.get('away_score')
    description = request.json.get('description')
    if not match_id or not title:
        return jsonify({'error': 'Please provide matchId and title'}), 400

    resp = client.put_item(
        TableName=MATCHES_TABLE,
        Item={
            'matchId': {'S': match_id },
            'title': {'S': title },
            'home': {'S': home },
            'away': {'S': away },
            'home_score': {'S': home_score },
            'away_score': {'S': away_score },
            'description': {'S': description }
        }
    )

    return jsonify({
        'matchId': match_id,
        'title': title,
        'home': home,
        'away': away,
        'home_score': home_score,
        'away_score': away_score,
        'description': description
    })