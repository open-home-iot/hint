export class Utility {

  static getCSRFToken() {
    const COOKIES = document.cookie.split(';');
    let csrfToken;
    for (let cookie of COOKIES) {
      cookie = cookie.trim();
      const RE = new RegExp('^csrftoken');
      if (RE.test(cookie)) {
        csrfToken = decodeURIComponent(cookie.substr(10, cookie.length)); // remove csrftoken=
        break;
      }
    }
    //console.log("Got CSRF Token: ", csrfToken);

    return csrfToken;
  }

  static generateRandomID(): string {
    const MAX = 100000;
    const MIN = 1;
    return String(Math.floor(Math.random() * (MAX - MIN + 1)) + MIN);
  }
}
