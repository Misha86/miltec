function wopen(link,wi,he){var width=wi;var height=he;var l=(screen.availWidth-width)/2;var t=(screen.availHeight-height)/2;wincom=window.open(link,"oswin","toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=0,width="+wi+",height="+he+",screenX="+l+",screenY="+t+",left="+l+",top="+t);if(wincom){wincom.focus();}else{alert(statustext);}}function dellink(link,btext){Check=confirm(btext);if(Check==false){return;}else{window.open(link,'_self');}}function changebutton(s){window.Bestellung.obutton.value="Bitte warten ... und diesen Button nur 1x klicken !!!!";if(SEND==1){alert("Sie haben die Bestellung bereits abgeschickt, bitte warten Sie auf Antwort des Shop-Servers !");return false;}else{SEND=1;return true;}}function fielddel(f){if(f.value==f.defaultValue){f.value="";}}function field_delete(f){if(f.value!=""){f.value="";}}function fieldset(f){if(f.value==""){f.value=f.defaultValue;}}function fieldemp(f){if(f.sbeg){if(f.sbeg.value==f.sbeg.defaultValue){f.sbeg.value="";}}}function tabbgcolor(tabid,hrefid,col1,col2){tabid.style.backgroundColor=col1;hrefid.style.color=col2;}function header_nav_color(zelle,link,hintergrund,schriftfarbe){if(document.getElementById(zelle)){document.getElementById(zelle).style.backgroundColor=hintergrund;}else if(document.getElementById(link)){document.getElementById(link).style.color=schriftfarbe;}}function changecolor_nav(zelle,farbe,sperrfarbe){if(document.getElementById(zelle)){var zellenfarbe=document.getElementById(zelle).style.backgroundColor;zellenfarbe=zellenfarbe.toLowerCase();sperrfarbe1=sperrfarbe.toLowerCase();sperrfarbe2=HexToNum(sperrfarbe1);if(zellenfarbe!=sperrfarbe1&&zellenfarbe!=sperrfarbe2){document.getElementById(zelle).style.backgroundColor=farbe;}}}function changecolor_nav_left(istfarbe,neuefarbe,sperrfarbe){var zellenfarbe=istfarbe;zellenfarbe=zellenfarbe.toLowerCase();sperrfarbe1=sperrfarbe.toLowerCase();sperrfarbe2=HexToNum(sperrfarbe1);if(zellenfarbe!=sperrfarbe1&&zellenfarbe!=sperrfarbe2){return neuefarbe;}else{return istfarbe;}}function choice_color(values){document.os_detail_view.variant.value=values;}function HexToNum(hexcode){if(hexcode.length!=7)return'nicht gueltig';tens=MakeNum(hexcode.substring(1,2));ones=MakeNum(hexcode.substring(2,3));paar1=(tens*16)+(ones*1);tens=MakeNum(hexcode.substring(3,4));ones=MakeNum(hexcode.substring(4,5));paar2=(tens*16)+(ones*1);tens=MakeNum(hexcode.substring(5,6));ones=MakeNum(hexcode.substring(6));paar3=(tens*16)+(ones*1);ergebnis='rgb('+paar1+', '+paar2+', '+paar3+')';return ergebnis;}function MakeNum(str){if((str>=0)&&(str<=9))return str;switch(str.toUpperCase()){case"A":return 10;case"B":return 11;case"C":return 12;case"D":return 13;case"E":return 14;case"F":return 15;return'X';}}function orderset(nid,cbox,control_field){var objre=document.getElementById(nid);var obj_control=document.getElementById(control_field);if(cbox.checked){objre.style.display="block";}else{if(obj_control.value!=''){objre.style.display="block";}else{objre.style.display="none";}}}function set_display_block(strID){var myObj=document.getElementById(strID);if(myObj){if(myObj.style.display=="none"){myObj.style.display="block";}}}