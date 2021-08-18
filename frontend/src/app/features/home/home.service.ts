import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

export interface Home {
  id: number;
  name: string;
}

export interface Room {
  id: number;
  home: number;
  name: string;
}

const HOMES_URL = window.location.origin + '/api/homes';

@Injectable()
export class HomeService {

  private homes: Home[] = [];
  private homeRoomMap = new Map(); // homeID => Room[]
  private roomMap = new Map();     // roomID => Room

  constructor(private httpClient: HttpClient) {
    this.httpClient.get(HOMES_URL)
      .subscribe(
        (homes: Home[]) => {
          this.replaceHomes(homes);
        },
        error => {
          console.error(error);
        }
      );
  }

  getHomes(): Home[] {
    return this.homes;
  }

  createHome(name: string): void {
    this.httpClient.post(HOMES_URL, {name})
      .subscribe(
        (home: Home) => {
          this.addHome(home);
        },
        error => {
          console.error(error);
        }
      );
  }


  getHomeRooms(homeID: number): Promise<Room[]> {
    if (this.homeRoomMap.has(homeID)) {
      return Promise.resolve(this.homeRoomMap.get(homeID));
    }

    // No rooms gotten yet, getting rooms...
    return new Promise<Room[]>((resolve, reject) => {
      this.httpClient.get(this.getHomeRoomsUrl(homeID))
        .subscribe(
          (rooms: Room[]) => {
            this.replaceRooms(homeID, rooms);
            resolve(this.homeRoomMap.get(homeID));
          },
          error => {
            reject(error);
          }
        );
    });
  }

  createRoom(homeID: number, roomName: string): Promise<Room> {
    return new Promise<Room>((resolve, reject) => {
      this.httpClient.post(this.getHomeRoomsUrl(homeID),
                     {name: roomName})
        .subscribe(
          (room: Room) => {
            this.addRoom(homeID, room);
            resolve(room);
          },
          error => {
            reject(error);
          }
        );
    });
  }

  getRoom(roomID: number) {
    return this.roomMap.get(roomID);
  }

  private addHome(home: Home) {
    this.homes.push(home);
  }

  private replaceHomes(homes: Home[]) {
    this.homes.length = 0;
    for (const HOME of homes) {
      this.addHome(HOME);
    }
  }

  private addRoom(homeID: number, room: Room) {
    this.homeRoomMap.get(homeID).push(room);
    this.roomMap.set(room.id, room);
  }

  private replaceRooms(homeID: number, rooms: Room[]) {
    if (!this.homeRoomMap.has(homeID)) {
      this.homeRoomMap.set(homeID, []);
    }

    // Maintain array reference
    this.homeRoomMap.get(homeID).length = 0;
    for (const ROOM of rooms) {
      this.addRoom(homeID, ROOM);
    }
  }

  private getHomeRoomsUrl(homeID: number) {
    return HOMES_URL + '/' + String(homeID) + '/rooms';
  }
}
