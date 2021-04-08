import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor(private httpClient: HttpClient) { }

  get(url: string) {
    return this.httpClient.get(url);
  }

  getWithOptions(url: string, options: {}) {
    return this.httpClient.get(url, options);
  }

  post(url: string, data: {}) {
    return this.httpClient.post(url, data);
  }

  put(url: string, data: {}) {
    return this.httpClient.put(url, data);
  }
}
