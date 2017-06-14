var message = document.getElementById("message")
var myDate = new Date();


/* Uur tussen 24:00:00 & 11:59:59 */
if ( myDate.getHours() < 12 )
{
    message.innerHTML = "<b>Goedemorgen,</b><br>laten we starten."
}
else /* Uur tussen 11:59:59 & 17:59:59 */
if ( myDate.getHours() >= 12 && myDate.getHours() <= 17 )
{
    message.innerHTML = "<b>Goedemiddag,</b><br>laten we starten."
}
else  /* Uur tussen 17:59:59 & 23:59:59 */
if ( myDate.getHours() > 17 && myDate.getHours() <= 24 )
{
    message.innerHTML = "<b>Goedeavond,</b><br>laten we starten."
}
else  /* Als het uur niet gevonden wordt */
{
    message.innerHTML = "<b>Hallo,</b><br>laten we starten."
}