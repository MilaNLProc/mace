from flask import render_template, redirect, flash, url_for, session
from app import app
from app.forms import MaceForms
from app.mace.utils import MaceInputs
from app.async_process import AsyncProcess


@app.route('/')
def init_page():
    """
    The main entry point "mace/" which redirects
    to "mace/index"
    """
    return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    This is the "mace/index". It
    - renders the index.html file
    - reads the user inputs from the form
    - checks inputs
    - transfers inputs to the async processor

    NOTE: Checks on required/optional inputs, correct format
        are performed in the Javascript
    """

    form = MaceForms()

    if form.validate_on_submit():

        # collect user inputs
        inputs = MaceInputs(form)

        # process, wordify, and send email
        async_job = AsyncProcess(inputs)
        async_job.run_async()

        return redirect(url_for('final'))

    return render_template('index.html', form=form)


@app.route('/final')
def final():
    nrow = session.get('nrow', None)
    nlabel = session.get('nlabel', None)
    return render_template('final.html', rows=nrow, labels=nlabel)


@app.errorhandler(413)
def file_too_big(error):
    flash('The file is too big')
    return redirect(url_for('index')), 413
