// main.js - handles UI interactions and AJAX predict

let selectedModelType = "custom_model"; // default
const fileInput = document.getElementById("file-input");
const previewBox = document.getElementById("image-preview");
const mainImg = document.getElementById("main-img");
const predictBtn = document.getElementById("predict-btn");
const modelButtons = document.querySelectorAll(".model-btn");
const classDropdown = document.getElementById("class-dropdown");
const nutritionContent = document.getElementById("nutrition-content");
const predictionOutput = document.getElementById("prediction-output");
const metricsCard = document.getElementById("metrics-card");
const confusionCard = document.getElementById("confusion");

// mark active model button
modelButtons.forEach(btn=>{
  btn.addEventListener("click", () => {
    modelButtons.forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    selectedModelType = btn.dataset.type;
  });
});
// activate default first button
document.getElementById("btn-custom").classList.add("active");

// show nutrition on class change
classDropdown.addEventListener("change", () => {
  const val = classDropdown.value;
  if(!val){ nutritionContent.innerHTML = "<p style='color:#888'>Select a class to view nutrition info...</p>"; return; }
  const info = NUTRITION[val];
  if(!info){ nutritionContent.innerHTML = "<p style='color:#888'>No data</p>"; return; }
  nutritionContent.innerHTML = `
    <div class="nut-card">
      <h4>${val.toUpperCase()}</h4>
      <p><strong>Calories:</strong> ${info.calories}</p>
      <p><strong>Protein:</strong> ${info.protein}</p>
      <p><strong>Carbs:</strong> ${info.carbohydrates}</p>
      <p><strong>Fiber:</strong> ${info.fiber}</p>
      <p><strong>Fat:</strong> ${info.fat}</p>
    </div>
  `;
});

// preview chosen file in the center
fileInput.addEventListener("change", async (e)=>{
  const file = e.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    // replace preview
    previewBox.innerHTML = `<img id="main-img" src="${reader.result}" alt="preview" class="fade">`;
  };
  reader.readAsDataURL(file);
});

// handle predict click
predictBtn.addEventListener("click", async ()=>{
  const file = fileInput.files[0];
  const selectedClass = classDropdown.value;

  if(!file){
    alert("Please upload an image first.");
    return;
  }
  if(!selectedClass){
    alert("Please select a class.");
    return;
  }

  predictBtn.disabled = true;
  predictBtn.textContent = "Predicting...";

  const fd = new FormData();
  fd.append("file", file);
  fd.append("model_type", selectedModelType);
  fd.append("selected_class", selectedClass);

  try{
    const res = await fetch("/predict", { method:"POST", body: fd });
    const data = await res.json();

    if(!data.success){
      predictionOutput.innerHTML = `<div style="color:red">Error: ${data.error}</div>`;
      return;
    }

    // show right-side prediction card
    let imgHtml = `<img src="${data.image_url}" alt="pred-thumb">`;
    let html = `<div class="prediction-card-inner">
        ${imgHtml}
        <p><strong>Predicted Class:</strong> <span style="color:#2b0f4b">${data.predicted_class}</span></p>
        <p><strong>Selected Class:</strong> ${data.selected_class}</p>
        <p><strong>Model Used:</strong> ${data.model_used}</p>
        <p><strong>Confidence:</strong> ${data.confidence}%</p>
        <p><strong>Accuracy:</strong> ${data.accuracy}</p>
        <p><strong>Precision:</strong> ${data.precision}</p>
        <p><strong>Recall:</strong> ${data.recall}</p>
      </div>`;
    predictionOutput.innerHTML = html;

    // metrics
    document.getElementById("m-accuracy").innerText = data.accuracy ?? "-";
    document.getElementById("m-precision").innerText = data.precision ?? "-";
    document.getElementById("m-recall").innerText = data.recall ?? "-";
    document.getElementById("m-f1").innerText = data.f1_score ?? "-";
    metricsCard.style.display = "block";

    // confusion matrix (if provided)
    if(data.confusion_matrix){
      const cm = data.confusion_matrix;
      // fill 3x3 if available
      for(let r=0;r<3;r++){
        for(let c=0;c<3;c++){
          const el = document.getElementById(`cm-${r}${c}`);
          if(el) el.innerText = (cm[r] && cm[r][c] !== undefined) ? cm[r][c] : "-";
        }
      }
      confusionCard.style.display = "block";
    } else {
      confusionCard.style.display = "none";
    }

    // ensure center preview is the uploaded image too
    previewBox.innerHTML = `<img src="${data.image_url}" alt="uploaded" class="fade">`;

    // done
  } catch(err){
    predictionOutput.innerHTML = `<div style="color:red">Error: ${err}</div>`;
  } finally {
    predictBtn.disabled = false;
    predictBtn.textContent = "Predict";
  }
});