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
   * HTTP REQUESTS
   *
   * Note that all observables returned by HTTP request functions need to be subscribed to in order to fire the request.
   */

  get(url: string): Observable<ResultSet> {
    return this.httpClient.get<ResultSet>(url);
  }

  post(url: string, body: {}) {
    // Add { observe: 'response' } to get more than just the response body back.
    return this.httpClient.post(url, body);
  }

  put() {}

  delete() {}
}
