from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.recipe import Recipe

@app.route('/recipes/new')
def new_recipe():
    if "id" not in session:
        return redirect('/')

    return render_template('recipeForm.html')

@app.route('/recipes/new/create', methods=["POST"])
def create_recipe():
    data = {
        "name":request.form ["name"],
        "description":request.form["description"],
        "instructions":request.form["instructions"],
        "date_made":request.form["date_made"],
        "under_30_min":request.form["under_30_min"],
        "user_id":session["id"]
    }

    if not Recipe.validate_recipe(data):
        return redirect('/recipes/new')

    Recipe.save(data)

    return redirect('/dashboard')

@app.route('/recipes/<recipe_id>')
def show_recipe(recipe_id):
    if "id" not in session:
        return redirect('/')

    data = {"id":recipe_id}
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('showRecipe.html', recipe=recipe)

@app.route('/recipes/edit/<recipe_id>')
def edit_recipe_form(recipe_id):
    if "id" not in session:
        return redirect('/')

    data = {"id":recipe_id}
    recipe = Recipe.get_recipe_by_id(data)

    if recipe.user_id != session["id"]:
        return redirect('/dashboard')

    return render_template('editRecipe.html', recipe=recipe)

@app.route('/recipes/update/<recipe_id>', methods=["POST"])
def edit_recipe(recipe_id):
    data = {
        "id":recipe_id,
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "under_30_min": request.form["under_30_min"],
        "date_made": request.form["date_made"]
    }

    if not Recipe.validate_recipe(data):
        return redirect(f'/recipes/edit/{recipe_id}')

    Recipe.update(data)

    return redirect('/dashboard')

@app.route ('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    if "id" not in session:
        return redirect('/')
    
    data = {"id":recipe_id}

    recipe = Recipe.get_recipe_by_id(data)

    if recipe.user_id != session["id"]:
        return redirect('/dashboard')

    Recipe.delete(data)
    
    return redirect('/dashboard')