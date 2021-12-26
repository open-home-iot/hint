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
}

export function* idGenerator() {
  let i = 0;
  while (true) {
    yield i++;
  }
}

/**
 * Generic error handling function.
 *
 * @param error
 */
export function handleError(error) {
  console.error(error);
}
