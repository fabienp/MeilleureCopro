import { Component } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { HttpClient, HttpParams, provideHttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { firstValueFrom } from 'rxjs';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  // Filtres stats
  filterType = 'city';
  filterValue = '';

  // Résultat stats
  result: any = null;
  error: string | null = null;

  // URL de l'annonce Bienici
  adUrl: string = '';
  addAdResult: any = null;

  constructor(private http: HttpClient) {}

  // Fonction pour récupérer les stats
  async submit() {
    this.error = null;
    this.result = null;

    const params = new HttpParams()
      .set('filter_type', this.filterType)
      .set('filter_value', this.filterValue);

    try {
      this.result = await firstValueFrom(
        this.http.get('http://127.0.0.1:8000/api/ads/stats', { params })
      );
    } catch (e: any) {
      console.error(e);
      this.error = 'Pas de résultats pour ce filtre';
    }
  }

  // Fonction pour ajouter une annonce Bienici
  async addAd() {
    this.addAdResult = null;

    if (!this.adUrl) {
      this.addAdResult = { success: false, message: 'Merci de fournir une URL Bienici' };
      return;
    }

    try {
      const data = await firstValueFrom(
        this.http.post('http://127.0.0.1:8000/api/ads', { url: this.adUrl })
      );

      // Succès : data contient l'annonce ajoutée
      this.addAdResult = { success: true, data };
      this.adUrl = ''; // reset champ input
    } catch (e: any) {
      // Essayer d'extraire le message d'erreur renvoyé par le back
      let message = 'Erreur lors de l\'ajout de l\'annonce';
      if (e?.error?.message) message = e.error.message;

      this.addAdResult = { success: false, message };
    }
  }
}

// ------------------------
// Bootstrap de l'application
// ------------------------
bootstrapApplication(App, {
  providers: [
    provideHttpClient() // nécessaire pour HttpClient
  ]
});
