import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Home, HomeService} from '../../home.service';
import {Hume, HumeService} from '../../../hume/hume.service';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';

@Component({
  selector: 'app-home-edit',
  templateUrl: './home-edit.component.html',
  styleUrls: ['./home-edit.component.scss']
})
export class HomeEditComponent implements OnInit {

  home: Home;
  // To avoid string interpolation error on page load.
  homeName = '';
  humes: Hume[];

  displayChangeHomeNameForm = false;
  changeHomeNameForm: FormGroup;

  constructor(private route: ActivatedRoute,
              private homeService: HomeService,
              private humeService: HumeService,
              private formBuilder: FormBuilder) { }

  ngOnInit(): void {
    this.changeHomeNameForm = this.formBuilder.group({
      name: ['', [Validators.required, Validators.maxLength(50)]]
    });

    this.homeService.getHome(Number(this.route.snapshot.params.id))
      .then(this.onGetHome.bind(this))
      .catch(this.onGetHomeFailed);

    this.humeService.getHomeHumes(Number(this.route.snapshot.params.id))
      .then(this.onGetHomeHumes.bind(this))
      .catch(this.onGetHomeHumesFailed);
  }

  toggleChangeHomeNameForm() {
    this.displayChangeHomeNameForm = !this.displayChangeHomeNameForm;
  }

  get name() { return this.changeHomeNameForm.get('name'); }

  changeHomeName() {
    if (this.home !== undefined) {
      this.homeService.changeHome(this.home, this.name.value)
        .then(this.onChangeHomeName.bind(this))
        .catch(this.onChangeHomeNameFailed);
    }
    this.toggleChangeHomeNameForm();
  }

  deleteHome() {
    console.log('deleting home');
  }

  private onGetHome(home: Home) {
    this.home = home;
    this.homeName = home.name;
  }

  private onGetHomeFailed(error) {
    console.error(error);
  }

  private onGetHomeHumes(humes: Hume[]) {
    this.humes = humes;
  }

  private onGetHomeHumesFailed(error) {
    console.error(error);
  }

  private onChangeHomeName(home: Home) {
    this.home = home;
    this.homeName = home.name;
  }

  private onChangeHomeNameFailed(error) {
    console.error(error);
  }
}
