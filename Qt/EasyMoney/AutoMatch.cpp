#include "AutoMatch.h"
#include "ui_AutoMatch.h"

AutoMatch::AutoMatch(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::AutoMatch)
{
    ui->setupUi(this);
}

AutoMatch::~AutoMatch()
{
    delete ui;
}
