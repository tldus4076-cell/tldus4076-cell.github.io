const orders = [
  { id: "B2B-2401", partner: "서울도서관", quantity: 42, amount: 756000, stock: 60, delivery: "normal" },
  { id: "B2B-2402", partner: "경기교육몰", quantity: 120, amount: 2160000, stock: 95, delivery: "normal" },
  { id: "B2B-2403", partner: "북스테이션", quantity: 18, amount: 324000, stock: 20, delivery: "address-check" },
  { id: "B2B-2404", partner: "문구플러스", quantity: 55, amount: 990000, stock: 0, delivery: "normal" },
  { id: "B2B-2405", partner: "기업복지몰", quantity: 33, amount: 594000, stock: 40, delivery: "normal" },
];

const currency = new Intl.NumberFormat("ko-KR", {
  style: "currency",
  currency: "KRW",
  maximumFractionDigits: 0,
});

function classifyOrder(order) {
  if (order.stock === 0) {
    return { label: "보류", className: "hold", reason: "재고 없음" };
  }

  if (order.stock < order.quantity) {
    return { label: "확인 필요", className: "check", reason: "주문 수량 대비 재고 부족" };
  }

  if (order.delivery === "address-check") {
    return { label: "확인 필요", className: "check", reason: "배송지 확인 필요" };
  }

  return { label: "출고 가능", className: "ready", reason: "정상" };
}

function renderOrders() {
  const rows = document.querySelector("#orderRows");
  rows.innerHTML = orders
    .map((order) => {
      const status = classifyOrder(order);
      return `
        <tr>
          <td>${order.id}</td>
          <td>${order.partner}</td>
          <td>${order.quantity.toLocaleString("ko-KR")}</td>
          <td>${currency.format(order.amount)}</td>
          <td>${order.stock.toLocaleString("ko-KR")}</td>
          <td><span class="status ${status.className}">${status.label}</span></td>
        </tr>
      `;
    })
    .join("");
}

function runAutomation() {
  const classified = orders.map((order) => ({ ...order, status: classifyOrder(order) }));
  const totalAmount = classified.reduce((sum, order) => sum + order.amount, 0);
  const readyOrders = classified.filter((order) => order.status.label === "출고 가능");
  const issueOrders = classified.filter((order) => order.status.label !== "출고 가능");

  document.querySelector("#totalAmount").textContent = currency.format(totalAmount);
  document.querySelector("#readyCount").textContent = `${readyOrders.length}건`;
  document.querySelector("#issueCount").textContent = `${issueOrders.length}건`;

  const issueLines = issueOrders
    .map((order) => `- ${order.id} / ${order.partner}: ${order.status.reason}`)
    .join("\n");

  document.querySelector("#shareMessage").textContent = `[B2B 주문 자동 분류 결과]\n총 주문: ${classified.length}건\n출고 가능: ${readyOrders.length}건\n확인 필요/보류: ${issueOrders.length}건\n총 주문금액: ${currency.format(totalAmount)}\n\n확인 필요 내역\n${issueLines}\n\n다음 액션\n1. 재고 부족 건은 물류/MD 담당자에게 입고 가능일 확인\n2. 배송지 확인 건은 거래처 담당자에게 주소 재확인\n3. 출고 가능 건은 운영툴에 업로드 후 정산 파일 생성`;
}

renderOrders();
document.querySelector("#runAutomation").addEventListener("click", runAutomation);
