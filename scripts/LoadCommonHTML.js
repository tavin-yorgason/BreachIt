SetElementHTML("navbar", "../templates/navbar.html");
SetElementHTML("footer", "../templates/footer.html");

function SetElementHTML(elementId, htmlFileName)
{
   fetch(htmlFileName)
      .then(response => response.text())
      .then(html =>
      {
         document.getElementById(elementId).innerHTML = html;
         
         document.dispatchEvent(new Event("headerLoaded"));
      });
}

