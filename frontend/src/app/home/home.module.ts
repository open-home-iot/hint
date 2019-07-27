import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HomeComponent} from './home.component';
import { HomeListComponent } from './home-list/home-list.component';

import { HomeRoutingModule } from './home-routing.module';

@NgModule({
  declarations: [
    HomeComponent,
    HomeListComponent
  ],
  imports: [
    HomeRoutingModule,
    CommonModule
  ],
  exports: [
    
  ]
})
export class HomeModule {}
