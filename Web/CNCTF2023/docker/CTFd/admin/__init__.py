import csv  # noqa: I001
import datetime
import os
from io import StringIO

from flask import Blueprint, abort
from flask import current_app as app
from flask import (
    jsonify,
    redirect,
    render_template,
    render_template_string,
    request,
    send_file,
    url_for,
)

admin = Blueprint("admin", __name__)

# isort:imports-firstparty
from CTFd.admin import challenges  # noqa: F401,I001
from CTFd.admin import notifications  # noqa: F401,I001
from CTFd.admin import pages  # noqa: F401,I001
from CTFd.admin import scoreboard  # noqa: F401,I001
from CTFd.admin import statistics  # noqa: F401,I001
from CTFd.admin import submissions  # noqa: F401,I001
from CTFd.admin import teams  # noqa: F401,I001
from CTFd.admin import users  # noqa: F401,I001
from CTFd.cache import (
    cache,
    clear_challenges,
    clear_config,
    clear_pages,
    clear_standings,
)
from CTFd.models import (
    Awards,
    Challenges,
    Configs,
    Notifications,
    Pages,
    Solves,
    Submissions,
    Teams,
    Tracking,
    Unlocks,
    Users,
    db,
)
from CTFd.utils import config as ctf_config
from CTFd.utils import get_app_config, get_config, set_config
from CTFd.utils.csv import dump_csv, load_challenges_csv, load_teams_csv, load_users_csv
from CTFd.utils.decorators import admins_only
from CTFd.utils.exports import background_import_ctf
from CTFd.utils.exports import export_ctf as export_ctf_util
from CTFd.utils.security.auth import logout_user
from CTFd.utils.uploads import delete_file
from CTFd.utils.user import is_admin


@admin.route("/admin", methods=["GET"])
def view():
    if is_admin():
        return redirect(url_for("admin.statistics"))
    return redirect(url_for("auth.login"))


@admin.route("/admin/plugins/<plugin>", methods=["GET", "POST"])
@admins_only
def plugin(plugin):
    if request.method == "GET":
        plugins_path = os.path.join(app.root_path, "plugins")

        config_html_plugins = [
            name
            for name in os.listdir(plugins_path)
            if os.path.isfile(os.path.join(plugins_path, name, "config.html"))
        ]

        if plugin in config_html_plugins:
            config_html = open(
                os.path.join(app.root_path, "plugins", plugin, "config.html")
            ).read()
            return render_template_string(config_html)
        abort(404)
    elif request.method == "POST":
        for k, v in request.form.items():
            if k == "nonce":
                continue
            set_config(k, v)
        with app.app_context():
            clear_config()
        return "1"


@admin.route("/admin/import", methods=["GET", "POST"])
@admins_only
def import_ctf():
    return redirect(url_for("admin.config"))


@admin.route("/admin/export", methods=["GET", "POST"])
@admins_only
def export_ctf():
    backup = export_ctf_util()
    ctf_name = ctf_config.ctf_name()
    day = datetime.datetime.now().strftime("%Y-%m-%d_%T")
    full_name = "{}.{}.zip".format(ctf_name, day)
    return send_file(
        backup, cache_timeout=-1, as_attachment=True, attachment_filename=full_name
    )


@admin.route("/admin/import/csv", methods=["POST"])
@admins_only
def import_csv():
    return redirect(url_for("admin.config"))


@admin.route("/admin/export/csv")
@admins_only
def export_csv():
    table = request.args.get("table")

    output = dump_csv(name=table)

    return send_file(
        output,
        as_attachment=True,
        max_age=-1,
        download_name="{name}-{table}.csv".format(
            name=ctf_config.ctf_name(), table=table
        ),
    )


@admin.route("/admin/config", methods=["GET", "POST"])
@admins_only
def config():
    # Clear the config cache so that we don't get stale values
    clear_config()

    configs = Configs.query.all()
    configs = {c.key: get_config(c.key) for c in configs}

    themes = ctf_config.get_themes()

    # Remove current theme but ignore failure
    try:
        themes.remove(get_config("ctf_theme"))
    except ValueError:
        pass

    force_html_sanitization = get_app_config("HTML_SANITIZATION")

    return render_template(
        "admin/config.html",
        themes=themes,
        **configs,
        force_html_sanitization=force_html_sanitization
    )


@admin.route("/admin/reset", methods=["GET", "POST"])
@admins_only
def reset():
    return render_template("admin/reset.html")
