import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class ApiService {
  API_URL = 'https://polarforecast-api-2022.azurewebsites.net' // 'http://127.0.0.1:8000'//
  constructor(private http: HttpClient) { }

  getRankings(event_key) {
    return this.http.get(this.API_URL + '/events/' + event_key + '/rankings');
  }
  getMatches(event_key: string, comp_level: string = null) {

    let endpoint = this.API_URL + '/events/' + event_key + '/matches'

    if (comp_level != null) {
      endpoint += '?comp_level=' + comp_level;
    }

    return this.http.get(endpoint);
  }

  getEvents() {
    return this.http.get(this.API_URL + '/events');
  }

  getEvent(event_key) {
    return this.http.get(this.API_URL + '/events/' + event_key);
  }
}
