from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Event, event_attendees
from app.extensions import db
from app.forms import EventForm
from app.utils.decorators import send_email


events_bp = Blueprint("events", __name__)


@events_bp.route("/home")
@login_required
def home():
    events = Event.query.all()
    return render_template("home.html", events=events)


@events_bp.route("/dashboard")
@login_required
def dashboard():
    events = Event.query.all()
    return render_template("dashboard.html", events=events)


@events_bp.route("/events", methods=["GET"])
@login_required
def list_events():
    search_query = request.args.get("search", "").strip()
    filter_date = request.args.get("date", "").strip()
    filter_location = request.args.get("location", "").strip()
    filter_availability = request.args.get("availability", "").strip()

    query = Event.query

    if search_query:
        query = query.filter(Event.title.ilike(f"%{search_query}%"))

    if filter_date:
        query = query.filter(Event.date == filter_date)

    if filter_location:
        query = query.filter(Event.location.ilike(f"%{filter_location}%"))

    events = query.all()

    for event in events:
        total_registered = db.session.query(event_attendees).filter_by(event_id=event.id).count()
        event.available_seats = event.max_attendees - total_registered

    if filter_availability == "available":
        events = [event for event in events if event.available_seats > 0]

    return render_template("dashboard.html", events=events, search_query=search_query)


@events_bp.route("/create_event", methods=["GET", "POST"])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            location=form.location.data,
            date=form.date.data,
            time=form.time.data,
            max_attendees=form.max_attendees.data,
            organizer_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()

        # uncomment this to test the email notification

        # send_email(
        #     subject="Event Created Successfully",
        #     recipients=[current_user.email],
        #     body=f"Hello {current_user.username},\n\nYou have successfully created the event '{event.title}' on {event.date} at {event.time}.\n\nLocation: {event.location}\n\nThank you!"
        # )

        flash("Event created successfully!", "success")
        return redirect(url_for("events.list_events"))
    return render_template("create_event.html", form=form)


@events_bp.route("/update_event/<int:event_id>", methods=["GET", "POST"])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)

    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.location = form.location.data
        event.date = form.date.data
        event.time = form.time.data
        event.max_attendees = form.max_attendees.data

        db.session.commit()
        flash("Event updated successfully!", "success")
        return redirect(url_for("events.list_events"))

    return render_template("update_event.html", form=form, event=event)


@events_bp.route("/delete_event/<int:event_id>", methods=["POST"])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    db.session.delete(event)
    db.session.commit()
    flash("Event deleted successfully!", "success")
    return redirect(url_for("events.list_events"))


@events_bp.route("/join_event/<int:event_id>", methods=["POST"])
@login_required
def join_event(event_id):
    event = Event.query.get_or_404(event_id)

    if current_user in event.attendees:
        flash("You have already joined this event.", "warning")
        return redirect(url_for("events.list_events"))

    if event.max_attendees and len(event.attendees) >= event.max_attendees:
        flash("This event is full!", "warning")
        return redirect(url_for("events.list_events"))

    event.attendees.append(current_user)
    db.session.commit()

    # uncomment this to test the email notification

    # send_email(
    #     subject="Event Registration Confirmed",
    #     recipients=[current_user.email],
    #     body=f"Hello {current_user.username},\n\nYou have successfully joined the event '{event.title}'.\n\nDate: {event.date}\nTime: {event.time}\nLocation: {event.location}\n\nSee you there!"
    # )

    flash("Successfully joined the event!", "success")
    return redirect(url_for("events.list_events"))
