//host = '192.168.1.106';	// home
//host = '140.116.215.188'; // lab
//host  = '140.116.215.181' //Rpi
//port = 8000;

host = "iot.eclipse.org"
port = 80
/* host = "140.116.245.218"
port = 8080  */

//topic = "FS_Website" +"@FS-" + getUUID();		// topic to subscribe to
topic = "FS_Website@FS-7bd70706-3641-c2e7-dee5-6acc343050b4";
useTLS = false;
username = null;
password = null;
// username = "jjolie";
// password = "aa";

// path as in "scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]"
//    defaults to "/mqtt"
//    may include query and fragment
//
// path = "/mqtt";
// path = "/data/cloud?device=12345";

cleansession = true;

function getUUID() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
      .toString(16)
      .substring(1);
  }
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
    s4() + '-' + s4() + s4() + s4();
}
