// 요소 선택
const modal = document.getElementById("profileModal");
const trigger = document.querySelector(".trigger-link");
const closeBtn = document.querySelector(".close");

// 링크 클릭 시 모달 표시
trigger.addEventListener("click", function (event) {
  event.preventDefault(); // 기본 동작 방지
  modal.style.display = "block";
});

// 닫기 버튼 클릭 시 모달 숨김
closeBtn.addEventListener("click", function () {
  modal.style.display = "none";
});

// 모달 배경 클릭 시 모달 숨김
window.addEventListener("click", function (event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});
