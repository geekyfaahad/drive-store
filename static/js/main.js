function incorrect_text() {
  Swal.fire({
    icon: "error",
    title: "Oops...",
    text: "Incorrect Username or Password",
  });
}

function alert_text() {
  Swal.fire({
    icon: "error",
    title: "Oops...",
    text: "User Already Exists!",
  });
}

function reset_text() {
  Swal.fire({
    icon: "info",
    title: "Reset Password Link",
    html: "Link has been sent to your Mail<br><br>Please Check 🙂",
  });
}

function verify_text() {
  Swal.fire({
    icon: "success",
    title: "Verification Link",
    html: `
      <p>Your account was successfully created.<br>
      Please follow the verification link that has been sent to your mail.</p><br>
      <a href="mailto:" style="text-decoration: none;">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="black" class="bi bi-envelope" viewBox="0 0 16 16">
  <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v.217l7 4.2 7-4.2V4a1 1 0 0 0-1-1zm13 2.383-4.708 2.825L15 11.105zm-.034 6.876-5.64-3.471L8 9.583l-1.326-.795-5.64 3.47A1 1 0 0 0 2 13h12a1 1 0 0 0 .966-.741M1 11.105l4.708-2.897L1 5.383z"/>
</svg> Go to Mail
      </a>
    `,
    confirmButtonText: "Okay",
  });
}

function profile() {
  // This will help you see what is passed to the function
  Swal.fire({
    html: `Hi <br><a href="/logout" style="color:black;text-decoration:none;">Logout</a>`,
    position: "center",
    width: 330,
  });
}

function sweet() {
  (async () => {
    const { value: email } = await Swal.fire({
      title: "Create Folder",
      input: "text",
      imageUrl: "/static/img/create.jpg",
      position: "center",
      inputPlaceholder: "Enter your Folder Name",
      width: 330,
    });

    if (email) {
      new_sweet(email);
    } else {
      Swal.fire({
        icon: "error",
        title: "Invalid input",
        text: "Please enter a valid folder name.",
      });
    }
  })();
}

function new_sweet(email) {
  console.log("Creating folder: " + email);
  request(email);
}

// Function to send an AJAX request to create a folder
function request(local) {
  fetch("/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ hk8: local }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.text();
    })
    .then((data) => {
      console.log("Response received:", data);
      window.location.href = "/";
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}



function options(folder_path, filename, file_size) {
  Swal.fire({
    position: "center",
    html: `
      <form action="/action_page.php" method="post">
        <a href="/file/download/${folder_path}/${filename}" download target="_blank" style="text-decoration: none; color: black;">
          <h3 id="yy5">Download</h3>
        </a>
        <a href="/file/delete/${folder_path}/${filename}" style="text-decoration: none; color: black;" onclick="return confirm('Are you sure you want to delete this file?');">
          <h3 id="yy5">Delete</h3>
        </a>
      </form>
    `,
    width: 300,
    showConfirmButton: false,
    showCloseButton: true,
  });
}

function upload_file(folder_path) {
  Swal.fire({
    width: 400,
    color: "#333",
    html: `
      <form action="/upload/${ folder_path }" id="upload_form" method="POST" enctype="multipart/form-data">
        <input type="file" name="file-input[]" id="file-input" required multiple accept=".txt, .pdf, .png, .jpg, .jpeg, .gif, .mp4, .mkv, .zip" style="display: inline;">
        <input type="submit" value="Upload">
      </form>
      <div class="progress" style="margin-top: 15px;">
        <div id="progressBar" class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;">0%</div>
      </div>
    `, // HTML content for Swal modal
    showConfirmButton: false
  });
}

$(document).ready(function () {
  $(document).on("submit", "form#upload_form", function (event) {
    event.preventDefault();

    // Fetch folder path from the form action
    var folderPath = $(this).attr("action");

    // File validation and form data setup
    var fileInput = $(this).find('input[type="file"]');
    var formData = new FormData($(this)[0]);
    var maxFileSize = 5000 * 1024 * 1024;
    var validTypes = [
      "text/plain", "application/pdf", "image/png", "image/jpeg", "image/gif",
      "video/mp4", "video/x-matroska", "application/zip"
    ];
    
    if (fileInput.get(0).files.length === 0) {
      Swal.fire({ icon: "warning", title: "No files selected", timer: 3000 });
      return;
    }

    // Validate file sizes and types
    for (let file of fileInput.get(0).files) {
      if (file.size > maxFileSize || !validTypes.includes(file.type)) {
        Swal.fire({ icon: "warning", title: `Invalid file: ${file.name}`, timer: 3000 });
        return;
      }
    }

    // Show the progress bar modal
    Swal.fire({
      title: "Uploading...",
      html: '<div class="progress"><div id="progressBar" class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;">0%</div></div>',
      allowOutsideClick: false,
      showConfirmButton: false,
      width: 400,
    });

    $.ajax({
      xhr: function () {
        var xhr = new window.XMLHttpRequest();
        xhr.upload.addEventListener("progress", function (e) {
          if (e.lengthComputable) {
            var percentComplete = Math.round((e.loaded / e.total) * 100);
            Swal.getHtmlContainer().querySelector("#progressBar").style.width = percentComplete + "%";
            Swal.getHtmlContainer().querySelector("#progressBar").textContent = percentComplete + "%";
          }
        });
        return xhr;
      },
      type: "POST",
      url: folderPath,
      data: formData,
      processData: false,
      contentType: false,
      success: function () {
        Swal.fire({
          icon: "success",
          title: "Your data has been successfully uploaded",
          timer: 2000,
          width: 400,
          showConfirmButton: false
        });
        console.log("File Uploaded Successfully")
        
        // Reset after success
        setTimeout(function () {
          window.location.reload();
        }, 2000);
      },
      error: function (xhr, status, error) {
        Swal.fire({ icon: "error", title: "Upload failed", text: error, timer: 3000 });
      }
    });
  });
});

function delete_folder() {
  Swal.fire({
    icon: "success",
    title: "Success",
    text: "Folder has been successfully deleted",
  }).then(() => {
    window.location.href = "/";
  });
}
