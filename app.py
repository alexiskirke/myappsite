from flask import Flask, render_template, jsonify, request, send_file
from meditation_video_generator import MeditationVideoGenerator
import os
import shutil
app = Flask(__name__)

# Sample data for portfolio apps
apps = [
    {
        "name": "Meditation Generator (AI)",
        "description": "An app that uses AI  to generate spoken meditation audio files with music or binaural beats.",
        "image": "Meditation.jpg",
        "link": "/meditation-generator"
    },
    {
        "name": "Long Book Author (AI)",
        "description": "Generates non-fiction books on any topic of 100 pages or more with mutliple chapters.",
        "image": "writersblock.jpg",
        "link": "/long-book-author"
    },
    {
        "name": "Screenplay Notes (AI)",
        "description": "Allows you to upload your screenplay and get detailed and smart notes on it from a specialized AI.",
        "image": "whatisyourstory.webp",
        "link": "/screenplay-notes"
    },
    # Add more apps as needed
]

@app.route('/')
def home():
    return render_template('index.html', apps=apps)

@app.route('/meditation-generator')
def meditation_generator():
    return render_template('meditation_generator.html')

@app.route('/generate_meditation', methods=['POST'])
def generate_meditation():
    try:
        # Extract form data
        api_key = request.form.get('api_key')
        topic = request.form.get('topic')
        length = int(request.form.get('length'))
        num_sentences = int(request.form.get('num_sentences'))
        two_voices = request.form.get('two_voices') == 'on'
        in_spanish = request.form.get('in_spanish') == 'on'
        binaural = request.form.get('binaural') == 'on'
        pan_voices = request.form.get('pan_voices') == 'on'

        # Initialize MeditationVideoGenerator
        mvg = MeditationVideoGenerator(
            length=length,
            api_key=api_key,  # Use the API key from the form
            topic=topic,
            binaural=binaural,
            num_sentences=num_sentences,
            two_voices=two_voices,
            in_spanish=in_spanish,
            force_working_dir_overwrite=True
        )

        # Add binaural options if selected
        if binaural:
            mvg.start_beat_freq = float(request.form.get('start_beat_freq'))
            mvg.end_beat_freq = float(request.form.get('end_beat_freq'))
            mvg.base_freq = float(request.form.get('base_freq'))

        # Add panning options if selected
        if pan_voices:
            mvg.balance_even = float(request.form.get('pan_voice1'))
            mvg.balance_odd = float(request.form.get('pan_voice2'))

        mvg.pipeline = {
            "texts": True,
            "audio_files": True,
            "combine_audio_files": True,
            "audio_fx": True,
            "background_audio": True,
            "image": False,
            "video": False,
            "keywords": False
        }
        # Generate meditation
        subsections, _ = mvg.run_meditation_pipeline()

        # Create a sanitized filename for the meditation
        sanitized_topic = topic[:20].replace(' ', '_')
        audio_filename = f"{sanitized_topic}_meditation_text_merged_fx_mixed.mp3"

        # Move the generated file to a location where it can be downloaded
        output_dir = os.path.join(app.static_folder, 'generated_meditations')
        os.makedirs(output_dir, exist_ok=True)
        shutil.move(audio_filename, os.path.join(output_dir, audio_filename))

        # Clean up the temporary directory
        if os.path.exists(sanitized_topic):
            shutil.rmtree(sanitized_topic)

        return jsonify({"success": True, "filename": audio_filename})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/download_meditation/<filename>')
def download_meditation(filename):
    return send_file(os.path.join(app.static_folder, 'generated_meditations', filename), as_attachment=True)

@app.route('/delete_meditation/<filename>', methods=['POST'])
def delete_meditation(filename):
    try:
        file_path = os.path.join(app.static_folder, 'generated_meditations', filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"success": True, "message": "File deleted successfully"})
        else:
            return jsonify({"success": False, "error": "File not found"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/long-book-author')
def long_book_author():
    return render_template('coming-soon.html')

@app.route('/screenplay-notes')
def screenplay_notes():
    return render_template('coming-soon.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    # Here you would typically process the form data and send an email
    # For now, we'll just return a success message
    return jsonify({"message": "Thank you for your message. We'll be in touch soon!"})

if __name__ == '__main__':
    app.run(debug=True)
