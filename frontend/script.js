
// ── ESTADO ──────────────────────────────────────────────────
let tipoPeleSelecionado = "oleosa";

// ── SELETOR DE TIPO DE PELE ──────────────────────────────────
document.querySelectorAll(".skin-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".skin-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    tipoPeleSelecionado = btn.dataset.value;
  });
});

// ── BOTÃO ANALISAR ───────────────────────────────────────────
document.getElementById("btnAnalisar").addEventListener("click", async () => {
  const ingredientes = document.getElementById("ingredientes").value.trim();

  if (!ingredientes) {
    shake(document.getElementById("ingredientes"));
    return;
  }

  const btn = document.getElementById("btnAnalisar");
  btn.querySelector(".btn-text").textContent = "Analisando...";
  btn.disabled = true;

  try {
    const res = await fetch("/analisar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ingredientes: ingredientes,
        tipo_pele: tipoPeleSelecionado
      })
    });

    const data = await res.json();
    exibirResultado(data);

  } catch (err) {
    alert("Erro ao conectar com o servidor. Verifique se o backend está rodando.");
  } finally {
    btn.querySelector(".btn-text").textContent = "Analisar produto";
    btn.disabled = false;
  }
});

// ── EXIBIR RESULTADO ─────────────────────────────────────────
function exibirResultado(data) {
  const secao = document.getElementById("resultado");
  secao.style.display = "block";
  secao.scrollIntoView({ behavior: "smooth", block: "start" });

  // Score
  const score = data.score;
  document.getElementById("scoreNum").textContent = `${score}/100`;

  setTimeout(() => {
    document.getElementById("scoreBar").style.width = `${score}%`;
  }, 100);

  let descricao = "";
  if (score >= 75) descricao = "Ótimo para sua pele! ✨";
  else if (score >= 50) descricao = "Razoável — fique de olho nos alertas.";
  else descricao = "Cuidado! Muitos ingredientes problemáticos.";
  document.getElementById("scoreDesc").textContent = descricao;

  // Métricas
  document.getElementById("mReconhecidos").textContent = data.ingredientes_reconhecidos;
  document.getElementById("mAlertas").textContent = data.alertas.length;
  document.getElementById("mNaoEncontrados").textContent = data.nao_encontrados.length;

  // Alertas
  const alertasSection = document.getElementById("alertasSection");
  const alertasList = document.getElementById("alertasList");
  alertasList.innerHTML = "";

  if (data.alertas.length > 0) {
    alertasSection.style.display = "block";
    data.alertas.forEach(a => {
      alertasList.innerHTML += `
        <div class="alerta-item">
          <div class="alerta-tipo">${a.tipo}</div>
          <div class="alerta-msg">${a.mensagem}</div>
        </div>
      `;
    });
  } else {
    alertasSection.style.display = "none";
  }

  // Detalhes dos ingredientes
  const detalhesSection = document.getElementById("detalhesSection");
  const detalhesList = document.getElementById("detalhesList");
  detalhesList.innerHTML = "";

  if (data.detalhes.length > 0) {
    detalhesSection.style.display = "block";
    data.detalhes.forEach(item => {
      const s = item.score_usuario;
      const emoji = s >= 75 ? "🟢" : s >= 50 ? "🟡" : "🔴";
      const div = document.createElement("div");
      div.className = "detalhe-item";
      div.innerHTML = `
        <div class="detalhe-header">
          <span>${emoji}</span>
          <span class="detalhe-nome">${item.nome_popular || item.nome_inci}</span>
          <span class="detalhe-score">${s}/100</span>
        </div>
        <div class="detalhe-cat">${item.categoria}</div>
        <div class="detalhe-exp">${item.explicacao}</div>
      `;
      div.addEventListener("click", () => div.classList.toggle("open"));
      detalhesList.appendChild(div);
    });
  } else {
    detalhesSection.style.display = "none";
  }

  // Não encontrados
  const naoSection = document.getElementById("naoEncontraSection");
  if (data.nao_encontrados.length > 0) {
    naoSection.style.display = "block";
    document.getElementById("naoEncontradosList").textContent =
      data.nao_encontrados.join(", ");
  } else {
    naoSection.style.display = "none";
  }
}

// ── ANIMAÇÃO DE ERRO (SHAKE) ─────────────────────────────────
function shake(el) {
  el.style.animation = "none";
  el.style.border = "1.5px solid #C97490";
  setTimeout(() => { el.style.border = ""; }, 1500);
}


// ── OCR: UPLOAD DE FOTO ──────────────────────────────────────
document.getElementById("uploadArea").addEventListener("click", () => {
  document.getElementById("fotoInput").click();
});

document.getElementById("fotoInput").addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const area = document.getElementById("uploadArea");
  area.classList.add("carregando");
  area.querySelector(".upload-texto").textContent = "Lendo o rótulo...";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/ocr", { method: "POST", body: formData });
    const data = await res.json();

    if (data.sucesso && data.ingredientes) {
      document.getElementById("ingredientes").value = data.ingredientes;
      area.querySelector(".upload-texto").textContent = "✅ Ingredientes extraídos! Confira e clique em Analisar.";
    } else {
      area.querySelector(".upload-texto").textContent = "⚠️ Não consegui ler. Tente uma foto mais nítida.";
    }
  } catch {
    area.querySelector(".upload-texto").textContent = "❌ Erro ao processar a imagem.";
  } finally {
    area.classList.remove("carregando");
  }
});