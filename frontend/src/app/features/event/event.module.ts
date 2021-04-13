import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

// COMPONENTS

// SERVICES
import { EventService } from './event.service';

// MODULES
import { EventRoutingModule } from './event-routing.module';


@NgModule({
  declarations: [],
  imports: [
    EventRoutingModule,
    CommonModule,
    FormsModule
  ],
  exports: [],
  providers: [EventService]
})
export class EventModule {}
