export class Utility {

  static getCSRFToken() {
    const cookies = document.cookie.split(';');
    let csrfToken;
    for (let cookie of cookies) {
      cookie = cookie.trim();
      const re = new RegExp('^csrftoken');
      if (re.test(cookie)) {
        csrfToken = decodeURIComponent(cookie.substr(10, cookie.length)); // remove csrftoken=
        break;
      }
    }
    console.log("Got CSRF Token: ", csrfToken);

    return csrfToken;
  }
}
