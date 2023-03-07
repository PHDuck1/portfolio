const previewContainer = document.querySelector('#preview-container');
const fileInput = document.querySelector('#id_file_field');
const convertButton = document.getElementById('convert-btn');
let orderObj = {}

fileInput.addEventListener('change', () => {
  previewContainer.innerHTML = '';

  for (let i=0; i < fileInput.files.length ; i++) {
    const file = fileInput.files[i]
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      const img = document.createElement('img');
      img.src = reader.result;

      const span = document.createElement('span');

      orderObj[file.name] = i;

      span.textContent = file.name;

      const div = document.createElement('div');
      div.classList.add('preview-item');
      div.appendChild(img);
      div.appendChild(span);
      previewContainer.appendChild(div);
    }
  }
});

convertButton.addEventListener('click', function() {
    let myJsonString = JSON.stringify(orderObj);
    let hiddenField = document.querySelector('input[name="image_previews"]');
    hiddenField.value = myJsonString;
});
