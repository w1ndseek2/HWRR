var wrapper = document.getElementById("signature-pad");
var clearButton = wrapper.querySelector("[data-action=clear]");
var undoButton = wrapper.querySelector("[data-action=undo]");
var savePNGButton = wrapper.querySelector("[data-action=save-png]");
var returnDataButton = wrapper.querySelector("[data-action=return-data]");
var canvas = wrapper.querySelector("canvas");
var signaturePad = new SignaturePad(canvas, {
  backgroundColor: 'rgb(255, 255, 255)'
});
function resizeCanvas() {
  var ratio = Math.max(window.devicePixelRatio || 1, 1);
  canvas.width = canvas.offsetWidth * ratio;
  canvas.height = canvas.offsetHeight * ratio;
  canvas.getContext("2d").scale(ratio, ratio);
  signaturePad.clear();
}
window.onresize = resizeCanvas;
resizeCanvas();

function download(dataURL, filename) {
  if (navigator.userAgent.indexOf("Safari") > -1 && navigator.userAgent.indexOf("Chrome") === -1) {
    window.open(dataURL);
  } else {
    var blob = dataURLToBlob(dataURL);
    var url = window.URL.createObjectURL(blob);

    var a = document.createElement("a");
    a.style = "display: none";
    a.href = url;
    a.download = filename;

    document.body.appendChild(a);
    a.click();

    window.URL.revokeObjectURL(url);
  }
}

// One could simply use Canvas#toBlob method instead, but it's just to show
// that it can be done using result of SignaturePad#toDataURL.
function dataURLToBlob(dataURL) {
  // Code taken from https://github.com/ebidel/filer.js
  var parts = dataURL.split(';base64,');
  var contentType = parts[0].split(":")[1];
  var raw = window.atob(parts[1]);
  var rawLength = raw.length;
  var uInt8Array = new Uint8Array(rawLength);

  for (var i = 0; i < rawLength; ++i) {
    uInt8Array[i] = raw.charCodeAt(i);
  }

  return new Blob([uInt8Array], { type: contentType });
}

clearButton.addEventListener("click", function (event) {
  signaturePad.clear();
});

undoButton.addEventListener("click", function (event) {
  var data = signaturePad.toData();

  if (data) {
    data.pop(); // remove the last dot or line
    signaturePad.fromData(data);
  }
});

savePNGButton.addEventListener("click", function (event) {
  if (signaturePad.isEmpty()) {
    alert("Please provide a signature first.");
  } else {
    var dataURL = signaturePad.toDataURL();
    download(dataURL, "signature.png");
  }
});
returnDataButton.addEventListener("click", function (event) {
  if (signaturePad.isEmpty()) {
    alert("Please provide a signature first.");
  } else {
    var dataURL = signaturePad.toData();
    $.ajax({
      type: 'POST',
      url: '/api/submit',
      data: JSON.stringify(dataURL),
      dataType: 'json',
      contentType: 'application/json',
      complete: function (a) {
        if (a.status === 200) {
          var json = JSON.parse(a.responseText)
          if (json['status'] != 0) {
            console.log(json['message'])
            window.location.href = "/page/error";
          }
          json = json['content']
          switch(json['action']){
            case 'register':
              if(json['finished']) location.href = "/page/success"
              else clearButton.click()
              break
            case 'login':
              if (json['result']) location.href = "/page/index"
              else {
                alert('登陆失败')
                location.href = "/page/login"
              }
              break
            case 'optimize':
              console.log(json['result'])
              clearButton.click()
              break
            case 'approve':
              console.log(json['result'])
              if(json['result']){
                $.ajax({
                  type: 'POST',
                  url: '/api/request/save_signature',
                  data: {
                    'data': signaturePad.toDataURL('image/png')
                  },
                  complete: function(a) {
                    alert('成功')
                    history.back()
                  }
                })
              }
              else clearButton.click()
              break
            default:
              location.href = "/page/error"
          }
        } else {
          window.location.href = "/page/error";
        }
      }
    })
    //download(JSON.stringify(dataURL), "signature.json");
  }
});


