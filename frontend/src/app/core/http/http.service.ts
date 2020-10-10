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

  post(url: string, data: {}) {
    console.log("Sending HTTP POST request");
    return this.httpClient.post(url, data);
  }
}
