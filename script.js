const PRICES = { lomitoClasico: 25000, lomitoMixto: 30000, hamburguesa: 38000, delivery: 10000 };
const formatGs = (n) => `Gs ${n.toLocaleString('es-PY')}`;

const publicUrl = window.location.href.split('#')[0];
document.getElementById('publicUrl').textContent = publicUrl;
document.getElementById('whatsappShare').href = `https://wa.me/?text=${encodeURIComponent('¡Hola! Te comparto el link para hacer tu pedido en Lomi & Burger: ' + publicUrl)}`;

document.getElementById('orderForm').addEventListener('submit', (e) => {
  e.preventDefault();
  const qtyClasico = Math.max(0, parseInt(document.getElementById('lomitoClasico').value || 0, 10));
  const qtyMixto = Math.max(0, parseInt(document.getElementById('lomitoMixto').value || 0, 10));
  const qtyBurger = Math.max(0, parseInt(document.getElementById('hamburguesa').value || 0, 10));
  const delivery = document.querySelector('input[name="delivery"]:checked').value === 'si';

  let total = 0;
  const lines = [];

  if (qtyClasico > 0) { const s = qtyClasico * PRICES.lomitoClasico; total += s; lines.push(`${qtyClasico} x Lomito Clásico = ${formatGs(s)}`); }
  if (qtyMixto > 0) { const s = qtyMixto * PRICES.lomitoMixto; total += s; lines.push(`${qtyMixto} x Lomito solo carne mixta = ${formatGs(s)}`); }
  if (qtyBurger > 0) { const s = qtyBurger * PRICES.hamburguesa; total += s; lines.push(`${qtyBurger} x Hamburguesa Simple = ${formatGs(s)}`); }
  if (delivery) { total += PRICES.delivery; lines.push(`Delivery = ${formatGs(PRICES.delivery)}`); }

  const result = document.getElementById('resultado');
  if (total === 0) {
    result.classList.remove('hidden');
    result.innerHTML = '<p><strong>Debes seleccionar al menos un producto o elegir delivery.</strong></p>';
    return;
  }

  const cliente = document.getElementById('cliente').value;
  const direccion = document.getElementById('direccion').value;
  const notas = document.getElementById('notas').value || 'Sin notas';

  result.classList.remove('hidden');
  result.innerHTML = `
    <h3>Pedido confirmado para ${cliente}</h3>
    <p><strong>Dirección:</strong> ${direccion}</p>
    <p><strong>Notas:</strong> ${notas}</p>
    <p><strong>Delivery:</strong> ${delivery ? 'Sí' : 'No'}</p>
    <ul>${lines.map((l) => `<li>${l}</li>`).join('')}</ul>
    <p><strong>Total:</strong> ${formatGs(total)}</p>
  `;
});
