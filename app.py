from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
import os, json, random, datetime

# ------------------ APP CONFIG ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates")
)

UPLOAD_FOLDER = os.path.join(app.static_folder, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXT = {"png", "jpg", "jpeg", "gif"}

# ------------------ LOAD CLASS / NUTRITION DATA ------------------
CLASS_JSON = os.path.join(BASE_DIR, "class.json")
with open(CLASS_JSON, "r", encoding="utf-8") as f:
    nutrition_data = json.load(f)

# ------------------ MODEL FILE FINDER ------------------
def find_models(folder_name):
    folder_path = os.path.join(BASE_DIR, folder_name)
    if not os.path.isdir(folder_path):
        return []
    return [
        os.path.join(folder_path, fn)
        for fn in sorted(os.listdir(folder_path))
        if fn.lower().endswith((".h5", ".keras", ".hdf5"))
    ]

# ------------------ MODEL INDEX ------------------
model_index = {
    "custom_model": find_models("custom_models"),
    "resnet_model": find_models("resnet_models"),
    "vgg_model": find_models("vgg_models"),
}

# ------------------ MODEL NAME MAP ------------------
MODEL_NAME_MAP = {
    "custom_model": "Custom CNN Model",
    "resnet_model": "ResNet50 Model",
    "vgg_model": "VGG16 Model"
}

# ------------------ HELPERS ------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

# Mock evaluation metrics (demo purpose)
default_metrics = {
    "accuracy": 0.9,
    "precision": 0.75,
    "recall": 0.8,
    "f1_score": 0.77,
    "confusion_matrix": [[160, 8, 2], [13, 131, 26], [7, 5, 49]]
}

# ------------------ ROUTES ------------------
@app.route("/")
def index():
    classes = sorted(nutrition_data.keys())

    sample_img_path = os.path.join(app.static_folder, "images", "sample_food.jpg")
    sample_image = (
        url_for("static", filename="images/sample_food.jpg")
        if os.path.exists(sample_img_path)
        else None
    )

    return render_template(
        "index.html",
        classes=classes,
        nutrition=nutrition_data,
        sample_image=sample_image,
        model_index=model_index
    )

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("file")
    selected_class = request.form.get("selected_class", "")
    model_type = request.form.get("model_type")

    print("DEBUG model_type received:", model_type)

    if not file or file.filename == "":
        return jsonify(success=False, error="No file uploaded.")

    if not allowed_file(file.filename):
        return jsonify(success=False, error="Invalid file type.")

    # Save uploaded image
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S_") + secure_filename(file.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    image_url = url_for("static", filename=f"uploads/{filename}")

    # ------------------ MODEL SELECTION ------------------
    available_models = model_index.get(model_type, [])

    if available_models:
        model_used = os.path.basename(available_models[0])
    else:
        model_used = MODEL_NAME_MAP.get(model_type, f"Unknown Model ({model_type})")

    # ------------------ MOCK PREDICTION ------------------
    predicted_class = selected_class or random.choice(list(nutrition_data.keys()))
    confidence = round(random.uniform(55.0, 98.0), 2)
    metrics = default_metrics

    # ------------------ RESPONSE ------------------
    response = {
        "success": True,
        "image_url": image_url,
        "predicted_class": predicted_class,
        "selected_class": selected_class,
        "model_used": model_used,
        "confidence": f"{confidence}",
        "accuracy": metrics["accuracy"],
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "f1_score": metrics["f1_score"],
        "confusion_matrix": metrics["confusion_matrix"]
    }

    return jsonify(response)

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)
