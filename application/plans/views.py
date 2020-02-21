from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.plans.models import Plan
from application.plans.forms import PlanForm
from application.streets.models import Street

@app.route("/myplans", methods=["GET"])
 #@login_required
def myplan_index():
    
    return render_template("/plans/plans.html", plans = Plan.query.all())
    

@app.route("/myplans/newplan", methods=["POST", "GET"])
# @login_required
def plan_add():

    streets = Street.query.all()
    street_list = [(s.id, s.name) for s in streets]

    form = PlanForm(request.form)
    form.street.choices = street_list

    if request.method == "GET":
        return render_template("plans/newplan.html", form = form)

    if request.method == "POST":


        new_plan = Plan()

        new_plan.completed = False
        new_plan.plandate = form.plandate.data
        new_plan.street_id = form.street.data
        new_plan.account_id = current_user.id

        db.session().add(new_plan)
        db.session().commit()

        return redirect(url_for("myplan_index"))

@app.route("/myplans/<plan_id>/", methods=["POST"])
def plan_set_completed(plan_id):

    p = Plan.query.get(plan_id)
    p.completed = True
    db.session().commit()

    return redirect(url_for("myplan_index"))

@app.route("/myplans/delete/<plan_id>", methods=["POST"])
def delete_plan(plan_id):

    p = Plan.query.get(plan_id)
    db.session.delete(p)
    db.session.commit()

    return redirect(url_for("myplan_index"))

    


    



    
