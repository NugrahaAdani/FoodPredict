const CIRCLE_CIRCUMFERENCE = 301.59;

export function buildResultViewModel(payload) {
  const label = payload?.prediction?.label ?? "-";
  const recommendationText =
    payload?.recommendation?.text ?? "Recommendation text tidak tersedia.";
  const nutrition = payload?.nutrition ?? null;

  return {
    filename: payload?.filename ?? "-",
    label,
    recommendationText,
    summary: `Model berhasil mengenali gambar ini sebagai ${label}.`,
    nutrition,
  };
}

function setVisibility(element, visible) {
  element.classList.toggle("hidden", !visible);
}

function updateStatus(text, tone = "muted") {
  const status = document.getElementById("analysisStatus");
  status.textContent = text;
  status.className = "mt-4 text-sm leading-relaxed";

  if (tone === "error") {
    status.classList.add("text-red-200");
    return;
  }
  if (tone === "success") {
    status.classList.add("text-ijo");
    return;
  }
  status.classList.add("text-slate-400");
}

function resetPanels() {
  setVisibility(document.getElementById("emptyState"), false);
  setVisibility(document.getElementById("loadingState"), false);
  setVisibility(document.getElementById("errorState"), false);
  setVisibility(document.getElementById("analysisResult"), false);
}

function showIdleState() {
  resetPanels();
  setVisibility(document.getElementById("emptyState"), true);
  document.getElementById("resultHeading").textContent = "Belum ada hasil";
}

function showLoadingState() {
  resetPanels();
  setVisibility(document.getElementById("loadingState"), true);
  document.getElementById("resultHeading").textContent = "Memproses permintaan";
}

function showErrorState(message) {
  resetPanels();
  setVisibility(document.getElementById("errorState"), true);
  document.getElementById("resultHeading").textContent = "Prediksi gagal";
  document.getElementById("errorMessage").textContent = message;
}

function renderResult(payload) {
  const viewModel = buildResultViewModel(payload);

  resetPanels();
  setVisibility(document.getElementById("analysisResult"), true);

  document.getElementById("resultHeading").textContent = "Analisis selesai";
  document.getElementById("predictionLabel").textContent = viewModel.label;
  document.getElementById("predictionSummary").textContent = viewModel.summary;
  document.getElementById("recommendationText").textContent = viewModel.recommendationText;
  document.getElementById("fileNameValue").textContent = viewModel.filename;

  // Render nutrition information
  renderNutritionInfo(viewModel.nutrition);
}

function renderNutritionInfo(nutrition) {
  const nutritionSection = document.getElementById("nutritionInfo");
  
  if (!nutrition) {
    nutritionSection.innerHTML = `
      <div class="rounded-3xl border border-yellow-400/25 bg-yellow-500/10 p-6">
        <p class="text-sm font-semibold tracking-[0.18em] text-yellow-200 uppercase">Info Gizi</p>
        <p class="mt-3 text-lg text-yellow-100">Data gizi tidak tersedia untuk bahan ini.</p>
      </div>
    `;
    return;
  }

  const calorieCategory = nutrition.kategori_kalori || "Tidak diketahui";
  const categoryColor = getCategoryColor(calorieCategory);

  nutritionSection.innerHTML = `
    <div class="rounded-3xl border border-emerald-400/25 bg-emerald-500/10 p-6">
      <div class="flex items-center justify-between mb-4">
        <p class="text-sm font-semibold tracking-[0.18em] text-emerald-200 uppercase">Info Gizi</p>
        <span class="rounded-full border border-emerald-400/35 bg-emerald-500/20 px-3 py-1 text-xs font-semibold text-emerald-200">
          ${calorieCategory}
        </span>
      </div>
      
      <div class="grid gap-3 sm:grid-cols-2">
        <div class="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p class="text-sm text-slate-400">Kalori</p>
          <p class="mt-1 text-xl font-bold text-white">${nutrition.kalori_kcal} <span class="text-sm font-normal text-slate-300">kcal</span></p>
        </div>
        
        <div class="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p class="text-sm text-slate-400">Protein</p>
          <p class="mt-1 text-xl font-bold text-white">${nutrition.protein_g} <span class="text-sm font-normal text-slate-300">g</span></p>
        </div>
        
        <div class="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p class="text-sm text-slate-400">Lemak</p>
          <p class="mt-1 text-xl font-bold text-white">${nutrition.lemak_g} <span class="text-sm font-normal text-slate-300">g</span></p>
        </div>
        
        <div class="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p class="text-sm text-slate-400">Karbohidrat</p>
          <p class="mt-1 text-xl font-bold text-white">${nutrition.karbohidrat_g} <span class="text-sm font-normal text-slate-300">g</span></p>
        </div>
        
        <div class="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p class="text-sm text-slate-400">Serat</p>
          <p class="mt-1 text-xl font-bold text-white">${nutrition.serat_g} <span class="text-sm font-normal text-slate-300">g</span></p>
        </div>
        
        <div class="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p class="text-sm text-slate-400">Kalsium</p>
          <p class="mt-1 text-xl font-bold text-white">${nutrition.kalsium_mg} <span class="text-sm font-normal text-slate-300">mg</span></p>
        </div>
      </div>
      
      <div class="mt-4 flex gap-2">
        ${nutrition.tinggi_protein ? '<span class="rounded-full bg-blue-500/20 px-3 py-1 text-xs font-semibold text-blue-200">Tinggi Protein</span>' : ''}
        ${nutrition.rendah_lemak ? '<span class="rounded-full bg-green-500/20 px-3 py-1 text-xs font-semibold text-green-200">Rendah Lemak</span>' : ''}
      </div>
      
      <p class="mt-4 text-sm text-slate-300">
        <strong>Catatan:</strong> Nilai gizi per 100 gram bahan. Data dapat bervariasi tergantung varietas dan cara pengolahan.
      </p>
    </div>
  `;
}

function getCategoryColor(category) {
  switch (category) {
    case "Rendah Kalori": return "green";
    case "Sedang Kalori": return "yellow";
    case "Tinggi Kalori": return "red";
    default: return "gray";
  }
}

async function requestPrediction(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("/predict", {
    method: "POST",
    body: formData,
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.detail || "Gagal memproses prediksi di server.");
  }
  return payload;
}

function initializeApp() {
  const fileInput = document.getElementById("imageUpload");
  const previewImage = document.getElementById("previewImage");
  const submitButton = document.getElementById("analisisButton");

  let selectedFile = null;

  showIdleState();

  fileInput.addEventListener("change", () => {
    selectedFile = fileInput.files?.[0] ?? null;

    if (!selectedFile) {
      previewImage.src = "";
      setVisibility(previewImage, false);
      updateStatus("Backend siap. Upload gambar untuk memulai prediksi.");
      showIdleState();
      return;
    }

    previewImage.src = URL.createObjectURL(selectedFile);
    setVisibility(previewImage, true);
    updateStatus(`File ${selectedFile.name} siap dianalisis.`);
    document.getElementById("resultHeading").textContent = "Siap diproses";
  });

  submitButton.addEventListener("click", async () => {
    if (!selectedFile) {
      updateStatus("Pilih gambar terlebih dahulu.", "error");
      showErrorState("Belum ada file yang dipilih untuk diprediksi.");
      return;
    }

    submitButton.disabled = true;
    updateStatus("Mengirim gambar ke backend dan menunggu hasil...", "muted");
    showLoadingState();

    try {
      const payload = await requestPrediction(selectedFile);
      renderResult(payload);
      updateStatus("Prediksi selesai dan recommendation berhasil dimuat.", "success");
    } catch (error) {
      showErrorState(error.message);
      updateStatus(error.message, "error");
    } finally {
      submitButton.disabled = false;
    }
  });
}

if (typeof document !== "undefined") {
  initializeApp();
}
