  document.addEventListener("DOMContentLoaded", function() {
    const updateCourseLink = document.querySelector(".update_course");
    const formContainer = document.querySelector(".tm-contact-form-container");
    let formVisible = false; 
  
    
    updateCourseLink.addEventListener("click", function(event) {
      event.preventDefault(); 
      if (formVisible) {
        formContainer.classList.add("hidden-form"); 
      } else {
        formContainer.classList.remove("hidden-form"); 
      }
      formVisible = !formVisible; 
    });
  });

  document.addEventListener("DOMContentLoaded", function() {
    const updateCourseLink = document.querySelector(".sua_course");
    const formContainer = document.querySelector(".tm-contact-form-container-update");
    let formVisible = false; 
  
    
    updateCourseLink.addEventListener("click", function(event) {
      event.preventDefault(); 
      if (formVisible) {
        formContainer.classList.add("hidden-form-update"); 
      } else {
        formContainer.classList.remove("hidden-form-update"); 
      }
      formVisible = !formVisible; 
    });
  });

    document.addEventListener("DOMContentLoaded", function() {
      const classLevelSelect = document.getElementById("class_level");
      const bandScoreGroup = document.getElementById("hidden_band-score-group_IELTS");
    
      classLevelSelect.addEventListener("change", function() {
        const selectedValue = classLevelSelect.value;
    
        if (selectedValue === "IELTS") {
          bandScoreGroup.style.display = "block";
        } else {
          bandScoreGroup.style.display = "none";
        }
      });
    });

  document.addEventListener("DOMContentLoaded", function() {
    const courseFeeInput = document.getElementById("course_fee");

    courseFeeInput.addEventListener("input", function() {
      let value = courseFeeInput.value;

      // Loại bỏ tất cả ký tự không phải số và dấu phẩy
      value = value.replace(/[^0-9,]/g, '');

      value = Number(value.split(",").join('')).toLocaleString('vi-VN');
      courseFeeInput.value = value;
    });
  });

  document.addEventListener("DOMContentLoaded", function() {
  const classLevelSelect = document.getElementById("class_level");
  const bandScoreGroupIELTS = document.getElementById("band-score-group_ielts");
  const bandScoreGroupTOEIC = document.getElementById("band-score-group_toeic");

  classLevelSelect.addEventListener("change", function() {
    const selectedValue = classLevelSelect.value;

    if (selectedValue === "IELTS") {
      bandScoreGroupIELTS.style.display = "block";
      bandScoreGroupTOEIC.style.display = "none";
    } else if (selectedValue === "TOEIC") {
      bandScoreGroupIELTS.style.display = "none";
      bandScoreGroupTOEIC.style.display = "block";
    } else {
      bandScoreGroupIELTS.style.display = "none";
      bandScoreGroupTOEIC.style.display = "none";
    }
  });
});


  if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
  }

  function confirmDelete(courseId) {
  const confirmation = confirm("Bạn có chắc chắn muốn xóa khóa học này?");
  if (confirmation) {
    // Nếu người dùng chọn "OK" trong hộp thoại xác nhận, thì mới thực hiện xóa
    deleteCourse(courseId);
  }
}

function deleteCourse(courseId) {
  fetch("/quanly/capnhatkhoahoc", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ courseId: courseId }),
  })
  .then((response) => {
    if (response.ok) {
      // Trang tự tải lại sau khi xóa thành công
      location.reload();
    } else {
      console.error("Request failed with status:", response.status);
    }
  })
  .catch((error) => {
    console.error("Error:", error);
  });
}

