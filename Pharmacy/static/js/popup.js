var modal=document.getElementById("myModal"),
body=document.getElementsByTagName("body"),
container=document.getElementById("myContainer"),
btnOpen=document.getElementById("myBtn"),
btnClose=document.getElementById("closeModal");
btnClose_2=document.getElementById("closeModal2");

btnOpen.onclick=function(){modal.className="Modal is-visuallyHidden",
setTimeout(function(){container.className="MainContainer is-blurred",
modal.className="Modal"},100),container.parentElement.className="ModalOpen"},

btnClose.onclick=function(){modal.className="Modal is-hidden is-visuallyHidden",
body.className="",container.className="MainContainer",container.parentElement.className=""},
btnClose_2.onclick=function(){modal.className="Modal is-hidden is-visuallyHidden",
body.className="",container.className="MainContainer",container.parentElement.className=""},
window.onclick=function(e){e.target==modal&&(modal.className="Modal is-hidden",
body.className="",
container.className="MainContainer",
container.parentElement.className="")};
