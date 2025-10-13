
const $ = (select, root = document) => root.querySelector(select);
const $$ = (select, root = document) => Array.from(root.querySelectorAll(select));

function toNumber(str){
	if (typeof str != "string") return null;
	const t = str.trim().replace(",", ".");
	if (t === "") return null;
	const num = Number(t);
	return Number.isFinite(num) ? num : null; 
}

function showError(message) {
	let box = $("#errors");
	if (!box) {
		box = document.createElement("div");
		box.id = "errors";
		box.style.marginTop = "10px";
    	box.style.padding = "10px";
    	box.style.border = "1px solid #e58";
    	box.style.background = "#fff4f6";
    	box.style.color = "#b42318";
    	box.style.borderRadius = "6px";
    	$(".input").appendChild(box);
	}
	box.textContent = message;
}

function clearError() {
	const box = $("#errors");
	if (box) box.remove();
}

const X_ALLOWED = [-3, -2, -1, 0, 1, 2, 3, 4, 5];
const R_ALLOWED = [1, 1.5, 2, 2.5, 3];
const Y_MIN = -5, Y_MAX = 3;

function getX() {
	const selected = $('.x-button.active');
	if (!selected) throw new Error("Выберите значение X.");
	const x = Number(selected.value);
	if (!X_ALLOWED.includes(x)) throw new Error("Недопустимое значение X");
	return x;
}

function setupXButtons() {
	const buttons = $$('.x-button');
	buttons.forEach(button => {
		button.addEventListener('click', () => {
			buttons.forEach(b => b.classList.remove('active'));
			button.classList.add('active');
		})
	})
}

function getR() {
	const checked = $$('input[type="checkbox"][name="r"]').filter(i => i.checked);
	if (checked.length != 1) throw new Error("Должно быть выбрано ровно 1 значение R");
	const r = Number(checked[0].value);
	if (!R_ALLOWED.includes(r)) throw new Error("Недопустимое значение R");
	return r
}

function getY() {
	const str = $("#y").value;
	const y = toNumber(str);
	if (y === null) throw new Error("Y должен быть числом");
	if (y < Y_MIN || y > Y_MAX) throw new Error(`Y должно быть числом от ${Y_MIN} до ${Y_MAX}`);
	return y;
}

function setupSingleCheckboxForR() {
	const boxes = $$('input[type="checkbox"][name="r"]');
	boxes.forEach( b => 
		b.addEventListener('change', () => {
			if (!b.checked) return;
			for (const o of boxes) if (o != b) o.checked = false;
		})
	);
}

async function sendRequest(x, y, r) {
	const params = new URLSearchParams({ x: String(x), y: String(y), r: String(r), fmt: "json" });
	const url = `/api/check?${params.toString()}`;
	const res = await fetch(url, {
		method: "GET",
		headers: { "Accept": "application/json" } 
	});
	if (!res.ok) {
		const text = await res.text().catch(() => "");
		throw new Error(`Ошибка HTTP ${res.status}: ${text || res.statusText}`);
	}
	const data = await res.json().catch(() => ({}));
	const payload = data.result;
	return {
		x: Number(payload.x),
		y: Number(payload.y),
		r: Number(payload.r),
		hit: Boolean(payload.hit),
		serverTime: payload.serverTime,
		workingTime: Number(payload.workingTime)
	};
}

function addRow({ x, y, r, hit, serverTime, workingTime }) {
  const tbody = $("#results-body");
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td>${x}</td>
    <td>${y}</td>
    <td>${r}</td>
    <td class="${hit ? "hit-yes" : "hit-no"}">${hit ? "да" : "нет"}</td>
    <td>${serverTime || "—"}</td>
    <td>${Number.isFinite(workingTime) ? workingTime : "—"}</td>
  `;
  tbody.prepend(tr);
}

function init() {

	setupSingleCheckboxForR();
	setupXButtons();

	const form = $("#check-form");
	if (!form) return;

	form.addEventListener("submit", async (e) => {
		e.preventDefault();
		clearError();
		try{
			const x = getX();
			const y = getY();
			const r = getR();
			const result = await sendRequest(x, y, r);
			addRow(result);
		} catch (err) {
			showError(err.message || String(err));
		}
	});

	form.addEventListener("reset", () => {
		clearError();

		$$('.x-button.active').forEach(b => b.classList.remove('active'));
	});
}

init();