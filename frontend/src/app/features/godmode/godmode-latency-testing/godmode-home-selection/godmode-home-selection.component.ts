import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {GodmodeService, PaginatedHomes} from '../../godmode.service';
import {Home} from '../../../home/home.service';
import {HANDLE_ERROR} from '../../../../core/utility';

@Component({
  selector: 'app-godmode-home-selection',
  templateUrl: './godmode-home-selection.component.html',
  styleUrls: ['./godmode-home-selection.component.scss']
})
export class GodmodeHomeSelectionComponent implements OnInit {

  @Output() homeSelected = new EventEmitter<Home>();

  homes: Home[] = [];

  next: string = null;
  previous: string = null;

  constructor(private godmodeService: GodmodeService) { }

  ngOnInit(): void {
  }

  listHomes(): void {
    this.godmodeService.listHomes()
      .then(response => this.handleResponse(response))
      .catch(error => HANDLE_ERROR(error));
  }

  nextHomes(): void {
    this.paginate(this.next);
  }

  previousHomes(): void {
    this.paginate(this.previous);
  }

  selectHome(home: Home) {
    this.homeSelected.emit(home);
  }

  private paginate(url: string): void {
    this.godmodeService.paginate(url)
      .then(response => this.handleResponse(response))
      .catch(error => HANDLE_ERROR(error));
  }

  private handleResponse(response: PaginatedHomes) {
    this.next = response.next;
    this.previous = response.previous;
    if (response.count != 0) {
      this.updateHomes(response.results);
    }
  }

  private updateHomes(homes: Home[]) {
    this.homes.length = 0;
    for (let home of homes) {
      this.homes.push(home);
    }
  }
}
