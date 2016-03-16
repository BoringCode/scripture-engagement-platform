import sqlite3
from flask import Flask, render_template, flash, redirect, url_for
from flask import g
from datetime import datetime, date

class Reading:
    def __init__(self, id, name, creationDate, text, reference):
        self.id = id
        self.name = name
        self.creationDate = creationDate
        self.text = text
        self.reference = reference

    def __str__(self):
        return self.name

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getCreationDate(self):
        return self.creationDate

    def getText(self):
        return self.text

    def getReference(self):
        return self.reference

    def find_reading(self):
        return g.db.execute('SELECT * FROM reading WHERE id = :self.id', {"id": self.id}).fetchone()

    def new_reading(name, BG_passage_reference):
        return g.db.execute('SELECT * FROM reading WHERE name = :name AND BG_passage_reference = :BG_passage_reference', {"name": name, "BG_passage_reference": BG_passage_reference}).fetchone()

    #add reading models for admins
    def add_reading(self):
        newReading = new_reading(self.name, self.reference)
        if newReading is None:
            query ='''
    INSERT INTO reading VALUES ((SELECT max(id) + 1 FROM reading), ?, datetime.now(), ?, ?)'''
            cursor = g.db.execute(query, (self.name, self.text, self.reference))
            return cursor.rowcount
        else:
            flash("Reading already exists,not added")


    #display individual reading
    def display_reading(self):
        indivReading=find_reading(self.id)
        return render_template('indiv_reading.html', indivReading= indivReading, form=IndivReading)

    #delete readings
    def delete_reading(self):
        delete_reading_content(self.id, False)
        delete_reading_post(self.id, False)
        delete_plan_reading(False, self.id)

        #delete_reading_post(id,False)
        return g.db.execute('DELETE FROM reading WHERE id = :self.id', {"id": self.id}).fetchone()

    def delete_reading_content(reading_id, content_id):
        return g.db.execute('DELETE FROM reading_content WHERE reading_id = :reading_id OR content_id = :content_id', {"reading_id": reading_id, "content_id": content_id}).fetchall()


    def delete_reading_post(reading_id,post_id):
        #return g.db.execute('DELETE FROM reading_post WHERE reading_id = :reading_id OR post_id = :post_id', {"reading_id": reading_id, "post_id": post_id}).fetchall()
        return True

    def delete_plan_reading(plan_id, reading_id):
        #return g.db.execute('DELETE FROM plan_reading WHERE reading_id = :reading_id OR plan_id = :plan_id', {"reading_id": reading_id, "plan_id": plan_id}).fetchall()
        return True

    #update reading
    def update_reading(self, name, text, reference):
        if name == '':
            name = self.name
        if text == '':
            text = self.text
        if reference == '':
            reference = self.reference
        query ='''
     UPDATE reading SET name=?, text=?, BG_passage_reference=? WHERE id = :self.id)'''
        return g.db.execute(query, (name, text, reference))
