import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { ResultSet } from './result-set.interface';
import { Observable } from 'rxjs/Observable';


@Injectable()
export class RequestService {
  csrfToken = '';

  constructor(private httpClient: HttpClient) {}

  getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      const re = new RegExp('^csrftoken');
      if (re.test(cookie)) {
        this.csrfToken = decodeURIComponent(cookie.substr(10, cookie.length)); // remove csrftoken=
        break;
      }
    }
    return this.csrfToken;
  }

  /**
   * GET request for DRF paginated responses.
   *
   * @param {string} url
   * @param {{}} options
   * @returns {Observable<ResultSet>}
   */

  get(url: string, options: {}): Observable<ResultSet> {
    return this.httpClient.get<ResultSet>(url, options);
  }

  /**
   * Generic get function for if result set is not a paginated one with the standard count, next, previous and results
   * fields.
   *
   * @param {string} url
   * @param {{}} options
   * @returns {Observable<{}>}
   */

  genericGet(url: string, options: {}): Observable<{}> {
    return this.httpClient.get<{}>(url, options);
  }

  post(url: string, body: {}) {
    // Add { observe: 'response' } to get more than just the response body back.
    return this.httpClient.post(url, body);
  }

  put() {}

  delete() {}
}
