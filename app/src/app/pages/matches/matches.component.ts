import { Component, OnInit, Pipe, ViewChild, HostListener } from '@angular/core';
import { DataSource } from '@angular/cdk/table';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { CdkTableModule } from "@angular/cdk/table";
import { MatSortModule, MatSort } from '@angular/material/sort';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-matches',
  templateUrl: './matches.component.html',
  styleUrls: ['./matches.component.scss']
})
export class MatchesComponent implements OnInit {

  displayedColumns: string[] = ['match_number', 'blue_score', 'blue_rp', 'red_score', 'red_rp', 'results'];

  dataSource = null;
  finalsDataSource = null;

  data: any = [];//this.ELEMENT_DATA;
  finalsData: any = [];

  @ViewChild('sort') sort: MatSort;
  @ViewChild('finalsSort') finalsSort: MatSort;

  public innerWidth: any;

  constructor(private api: ApiService) { }

  ngOnInit(): void {
    this.getMatches();
    this.data.sort = this.sort;
    this.finalsData.sort = this.finalsSort;
    this.innerWidth = window.innerWidth;
  }

  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.innerWidth = window.innerWidth;
  }

  getResponsiveMode() {
    return this.innerWidth < 800;
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
    //this.dataSource.sortingDataAccessor = (data, attribute) => data[attribute];
    this.finalsDataSource.sort = this.sort;
  }


  getMatches() {
    const event = localStorage.getItem('event');
    if (event != null) {
      this.api.getMatches(event, 'qm')
        .subscribe(data => {
          if ('data' in data) {
            data['data'].sort(function (a, b) {
              if (a.match_number < b.match_number) return -1;
              if (a.match_number > b.match_number) return 1;
              return 0;
            });
            this.data = data['data'];
            console.log(this.data);
            this.dataSource = new MatTableDataSource(this.data);
            this.dataSource.sort = this.sort;
            let elims = true;
            for (let i = 0; i < this.data.length; i++) {
              if (this.data[i]['comp_level'] != 'qm') {
                elims = false;
              }
              console.log(this.data[i]);
              //this.data[i]['match_number'] = String(this.data[i]['match_number']).padStart(3, '0');
            }
            if (elims) {
              this.getFinalsMatches();
            }

          }
        });
    }
  }

  getFinalsMatches() {
    const event = localStorage.getItem('event');
    if (event != null) {
      this.api.getMatches(event, 'elim')
        .subscribe(data => {
          if ('data' in data) {
            this.finalsData = data['data'];

            for (let i = 0; i < this.finalsData.length; i++) {
              let entry = this.finalsData[i];
              let comp_level = entry['comp_level']
              if (comp_level == 'f') {
                entry['match_order'] = 100 + entry['set_number'];
              } else if (comp_level == 'sf') {
                entry['match_order'] = 10 + entry['set_number'];
              } else if (comp_level == 'qf') {
                entry['match_order'] = entry['set_number'];
              }
            }

            console.log(this.finalsData);
            this.finalsDataSource = new MatTableDataSource(this.finalsData);
            this.finalsDataSource.sort = this.finalsSort;
          }
        });
    }
  }

  getWinner(match) {
    if (match['blue_score'] > match['red_score']) {
      return 'Blue'
    } else {
      return 'Red'
    }
  }

  getWinnerPoints(match) {
    if (match['blue_score'] > match['red_score']) {
      return Math.round(match['blue_score'])
    } else {
      return Math.round(match['red_score'])
    }
  }

}
