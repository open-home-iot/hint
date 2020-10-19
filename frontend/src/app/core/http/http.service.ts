import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  constructor(private httpClient: HttpClient) { }

  get(url: string) {
    console.log("Sending HTTP GET request");
    return this.httpClient.get(url);
  }

  getWithOptions(url: string, options: {}) {
    console.log("Sending HTTP GET request with options");
    return this.httpClient.get(url, options);
  }

  post(url: string, data: {}) {
    console.log("Sending HTTP POST request");
    return this.httpClient.post(url, data);
  }

  put(url: string, data: {}) {
    console.log("Sending HTTP PUT request");
    return this.httpClient.put(url, data);
  }
}
