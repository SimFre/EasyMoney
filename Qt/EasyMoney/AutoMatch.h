#ifndef AUTOMATCH_H
#define AUTOMATCH_H

#include <QDialog>

namespace Ui {
class AutoMatch;
}

class AutoMatch : public QDialog
{
    Q_OBJECT

public:
    explicit AutoMatch(QWidget *parent = 0);
    ~AutoMatch();

private:
    Ui::AutoMatch *ui;
};

#endif // AUTOMATCH_H
