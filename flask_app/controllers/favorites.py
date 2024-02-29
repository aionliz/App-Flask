from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.quote import Quote
from flask_app.models.favorite import Favorite


@app.route('/new/favorite/<int:quote_id>')
def new_favorite(quote_id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = session['user_id']

    # obtener la cita seleccionada
    quote = Quote.get_one({"id": quote_id})
    if not quote:
        flash("Quote not found", "error")
        return redirect('/quote')
    data = {
        "name": quote['name'],
        "message": quote['message'],
        "user_id": user_id
    }

    Favorite.save(data)

    @app.route('/quote', methods=['POST', 'GET'])
    def quote():
        if 'user_id' not in session:
            return redirect('/logout')
        data = {
            "id": session['user_id']
        }
        return render_template("quote.html", user=User.get_by_id(data), all_quotes=Quote.get_all(), all_favorites=Favorite.get_all())

    # agregar la cita a la tabla de favoritos
    @app.route('/add_to_favorites/<int:quote_id>')
    def add_to_favorites(quote_id):
        if 'user_id' not in session:
            return redirect('/logout')
        user_id = session['user_id']

        # obtener la cita seleccionada
        quote = Quote.get_one({"id": quote_id})
        if not quote:
            flash("Quote not found", "error")
            return redirect('/quote')
        data = {
            "name": quote.name,
            "message": quote.message,
            "user_id": user_id,
            "quote_id" : quote_id
        }
        # agregar la cita a la tabla de favoritos
        Favorite.save(data)
        print("added to favorites")

        # eliminar la cita de la tabla de citas
        Quote.destroy({"id": quote_id})

        return redirect('/favorite')

    return redirect('/favorite')


@app.route('/remover_from_favorites/<int:quote_id>')
def remove_from_favorites(quote_id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_id = session['user_id']

    # obtener la cita seleccionada
    favorite = Favorite.get_one({"id": quote_id})
    if not favorite:
        flash("Favorite not found", "error")
        return redirect('/quote')
    if favorite['user_id'] != user_id:
        flash("You are not allowed to remove this favorite", "error")
        return redirect('/quote')

    data = {
        "name": favorite['name'],
        "message": favorite['message'],
        "user_id": user_id
    }

    # agregar la cita a la tabla de citas

    Quote.save(data)

    # eliminar la cita de la tabla de favoritos
    Favorite.destroy({"id": quote_id})

    return redirect('/quote')


