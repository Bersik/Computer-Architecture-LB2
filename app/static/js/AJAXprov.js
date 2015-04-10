function  AJAXprov()
{
  var xmlhttp;
  var answServ;
  
  this.provXmlHttp = function()
  {
      var xmlhttp;
    try 
    {
          xmlhttp = new ActiveXObject('Msxml2.XMLHTTP');
      } 
    catch (e) 
    {
          try 
      {
  		  xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
  		} 
      catch (E) 
      {
            xmlhttp = false;
          }
      }
      if (!xmlhttp && typeof XMLHttpRequest!='undefined') 
    {
          xmlhttp = new XMLHttpRequest();
      }
    return xmlhttp;
  }

//первый - режим работы false/true (синх/асинх), 
//второй - тип запроса (POST/GET)
//третий - параметры для запроса (адрес, по которому нужно отправить запрос, 
//четвертый - необязательный аргумент, содержащий параметры для POST запроса
  this.sendAnsServ = function (modeWork, typeSend, adr, param, id, cb)
  {
    if(typeSend == 'G')
    {
      adr = adr + '?' + param;
      httpP.open('GET', adr, modeWork);
  	 	httpP.setRequestHeader('Cache-Control', 'no-cache, must-revalidate');
  		httpP.onreadystatechange = function()
  		{
        if (httpP.readyState == 4) 
    		{
          if(httpP.status == 200)
          {
            if(cb)
            {
              return httpP.responseText;
            }
          }
        }
      }
      httpP.send(null);
    }
    if(typeSend == 'P')
    {
      httpP.open('POST', adr, modeWork);
      httpP.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    	httpP.setRequestHeader('Cache-Control', 'post-check=0,pre-check=0, false');
    	httpP.setRequestHeader('Cache-Control',  'max-age=0, false');
    	httpP.setRequestHeader('Pragma', 'no-cache');
    	httpP.setRequestHeader('Cache-Control', 'no-cache, must-revalidate');
    	httpP.send(param);
      if(httpP.status == 200)
      {
        if(cb)
        {
          return httpP.responseText;
        }
      }
    }
  }
}
