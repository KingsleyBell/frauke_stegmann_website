import json
import os
import re

from flask import Flask, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from auth import requires_auth

# the all-important app variable:
application = Flask(__name__)


@application.route('/')
def home():
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    shows = [section for section in db if section['type'] == 'show']
    artists = [section for section in db if section['type'] == 'artist']
    return render_template(
        'index.html',
        shows=shows,
        artists=artists
    )


@application.route('/admin/', methods=['GET', 'POST'])
@requires_auth
def sections():
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    shows = [section for section in db if section['type'] == 'show']
    artists = [section for section in db if section['type'] == 'artist']
    if request.method == 'POST':  # Delete section
        section_id = request.form.get('section_id')

        section = [section for section in db if section['id'] == section_id][0]
        for image in section['images']:
            delete_image_file(image['url'])
        db.remove(section)

        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return jsonify({'success': True})
    else:
        return render_template('sections.html', shows=shows, artists=artists)


@application.route('/new_section/', methods=['GET', 'POST'])
@requires_auth
def new_section():
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    if request.method == 'POST':
        section_name = request.form.get('section')
        section_id = re.sub('[^A-Za-z0-9]+', '_', section_name).lower()
        section_type = request.form.get('type')
        section_dict = {
            'type': section_type,
            'name': section_name,
            'id': section_id,
            'text': '',
            'images': []
        }
        db.append(section_dict)
        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return redirect(url_for('sections'))
    else:
        return render_template('new_section.html')


@application.route('/edit_section/<string:section_id>/', methods=['GET', 'POST'])
@requires_auth
def edit_section(section_id):
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    section = [s for s in db if s['id'] == section_id][0]
    if request.method == 'POST':
        section_name = request.form.get('name')
        section_id = re.sub('[^A-Za-z0-9]+', '_', section_name).lower()
        section_type = request.form.get('type')
        section_text = request.form.get('text')

        section['name'] = section_name
        section['id'] = section_id
        section['type'] = section_type
        section['text'] = section_text

        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return redirect(url_for('sections'))
    else:
        return render_template('edit_section.html', section=section)


@application.route('/edit_image/<string:section_id>/<int:image_id>/', methods=['GET', 'POST'])
@requires_auth
def edit_image(section_id, image_id):
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    section = [s for s in db if s['id'] == section_id][0]
    image = [i for i in section['images'] if i['id'] == image_id][0]
    if request.method == 'POST':
        title = request.form.get('title')
        section_name = request.form.get('section')
        display_width = request.form.get('display_width')
        align = request.form.get('align')
        full_width = request.form.get('full_width') == "true"

        db_section = [s for s in db if s['name'] == section_name][0]
        db_section['images'].append(image)
        section['images'].remove(image)

        image["title"] = title
        image["display_width"] = display_width
        image["align"] = align
        image["full_width"] = full_width

        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return redirect(url_for('sections'))
    else:
        sections = [section['name'] for section in db]
        return render_template(
            'edit_image.html',
            image=image,
            section=section['name'],
            sections=sections
        )


@application.route('/delete_image/', methods=['POST'])
@requires_auth
def delete_image():
    section_id = request.form.get('section_id')
    image_id = int(request.form.get('image_id'))

    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    section = [s for s in db if s['id'] == section_id][0]
    image = [i for i in section['images'] if i['id'] == image_id][0]
    filename = image['url']

    section['images'].remove(image)
    delete_image_file(filename)

    with open(db_path, 'w') as db_write:
        db_write.write(json.dumps(db))

    return jsonify({'success': True})


@application.route('/upload/', methods=['GET', 'POST'])
@application.route('/upload/<string:section_id>/', methods=['GET', 'POST'])
@requires_auth
def upload(section_id=None):
    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())
    if request.method == 'POST':
        section = request.form.get('section')

        image_ids = []
        for s in db:
            image_ids += [image['id'] for image in s['images']]
        image_id = max(image_ids + [0]) + 1

        db_section = [s for s in db if s['id'] == section][0]

        title = request.form.get('title')
        display_width = request.form.get('display_width')
        align = request.form.get('align')
        full_width = request.form.get('full_width') == "true"

        image_file = request.files.get('file')
        file_extension = image_file.filename.split('.')[-1]
        subdir = f'{db_section["type"]}s'
        upload_folder = os.path.join(application.static_folder, f'images/uploads/{subdir}')
        filename = secure_filename(str(image_id) + '.' + file_extension)
        image_file.save(os.path.join(upload_folder, filename))

        image_dict = {
            "id": image_id,
            "url": f'{subdir}/{filename}',
            "title": title,
            "display_width": display_width,
            "align": align,
            "full_width": full_width
          }

        db_section['images'].append(image_dict)
        with open(db_path, 'w') as db_write:
            db_write.write(json.dumps(db))

        return redirect(url_for('sections'))
    else:
        sections = {section['name']: section['id'] for section in db}
        return render_template('upload.html', sections=sections, section=section_id)


@application.route('/new_home_image/', methods=['GET', 'POST'])
@requires_auth
def new_home_image():
    if request.method == 'POST':
        image_file = request.files.get('file')
        upload_folder = os.path.join(application.static_folder, 'images')
        filename = "home.jpg"
        image_file.save(os.path.join(upload_folder, filename))

        return redirect(url_for('sections'))
    else:
        return render_template('upload_file.html', form_label='New Home Image (must be jpg)')


@application.route('/shift_section_position', methods=['POST'])
def shift_section_position():
    section_id = request.form.get('section_id')
    shift = int(request.form.get('shift'))

    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())

    section = [s for s in db if s['id'] == section_id][0]
    type_db = [s for s in db if s['type'] == section['type']]
    section_index = db.index(section)
    section_type_index = type_db.index(section)

    if section_type_index == 0 and shift < 0:  # can't shift up if at top
        return jsonify({'success': False})
    if section_type_index == len(db) - 1 and shift > 0:  # Can't shift down if at bottom
        return jsonify({'success': False})

    swap_index = db.index(type_db[section_type_index + shift])

    db[section_index], db[swap_index] = db[swap_index], db[section_index]

    with open(db_path, 'w') as db_write:
        db_write.write(json.dumps(db))

    return jsonify({'success': True})


@application.route('/shift_image_position', methods=['POST'])
def shift_image_position():
    section_id = request.form.get('section_id')
    image_id = int(request.form.get('image_id'))
    shift = int(request.form.get('shift'))

    db_path = os.path.join(application.static_folder, 'db/db.json')
    db = json.loads(open(db_path, 'r').read())

    section = [s for s in db if s['id'] == section_id][0]
    image = [i for i in section['images'] if i['id'] == image_id][0]
    image_index = section['images'].index(image)

    if image_index == 0 and shift < 0:  # can't shift up if at top
        return jsonify({'success': False})
    if image_index == len(section['images']) - 1 and shift > 0:  # Can't shift down if at bottom
        return jsonify({'success': False})

    section['images'][image_index], section['images'][image_index + shift] = section['images'][image_index + shift], section['images'][image_index]

    with open(db_path, 'w') as db_write:
        db_write.write(json.dumps(db))

    return jsonify({'success': True})


def delete_image_file(filename):
    upload_folder = os.path.join(application.static_folder, 'images/uploads')
    os.remove(os.path.join(upload_folder, filename))


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=800)
