Hpc Command
======================================================================

High Performance Computing(HPC) allows to solve large complex problems in
engineering, science and business using applications that require very
high compute power and amplified bandwidth. The cloudmesh hpc command helps
to easily manage hpc clusters.

The manual page of the hpc command can be found at: `Hpc
<../man/man.html#hpc>`_

Before we get started, we can set the default hpc cluster or use the
--cluster option. To set the default hpc cluster::

    $ cm default cluster=comet
    set in defaults cluster=comet. ok.


hpc info
----------------------------------------------------------------------

Returns the state of partitions and nodes on the hpc cluster::

  $ cm hpc info
    +---------+-----------+-------+------------+-------+-------+----------------------------+---------------------+
    | cluster | partition | avail | timelimit  | nodes | state | nodelist                   | updated             |
    +---------+-----------+-------+------------+-------+-------+----------------------------+---------------------+
    | india   | xxxxx     | up    | 3-00:00:00 | 8     | idle  | b[009-016]                 | 2015-11-29 16:06:25 |
    | india   | yyyyy     | up    | 3-00:00:00 | 12    | idle  | d[001-012]                 | 2015-11-29 16:06:25 |
    | india   | zzzzz     | up    | 3-00:00:00 | 16    | idle  | i[81-84,86-89,91-95,97-99] | 2015-11-29 16:06:25 |
    +---------+-----------+-------+------------+-------+-------+----------------------------+---------------------+

hpc queue
----------------------------------------------------------------------

Reports the state of jobs or job sets::

    $ cm hpc queue
    +---------+---------+--------------+--------------------+-----------+----+------------+-------+---------------------+---------------------+
    | cluster | jobid   | partition    | name               | user      | st | time       | nodes | nodelist            | updated             |
    +---------+---------+--------------+--------------------+-----------+----+------------+-------+---------------------+---------------------+
    | india   | 1205397 | gpu-shared   | xxx                | x_user    | PD | 0:00       | 1     |                      | 2015-11-29 16:16:27 |
    | india   | 1267689 | compute      | yyy                | y_user    | PD | 0:00       | 1     |                      | 2015-11-29 16:16:27 |
    | india   | 1267690 | compute      | zzz                | y_user    | PD | 0:00       | 8     |                      | 2015-11-29 16:16:27 |
    | india   | 1267691 | compute      | lll                | y_user    | PD | 0:00       | 3     |                      | 2015-11-29 16:16:27 |
    | india   | 1267693 | compute      | mmm                | y_user    | PD | 0:00       | 1     |                      | 2015-11-29 16:16:27 |
    | india   | 1295159 | gpu          | nnnnnnn            | z_user    | CG | 1-00:00:03 | 1     | xxxxx-30-13          | 2015-11-29 16:16:27 |
    | india   | 1304301 | compute      | ooooooooooo        | y_user    | R  | 23:38:55   | 8     | yy-04-[20-21,63-68]  | 2015-11-29 16:16:27 |
    +---------+---------+--------------+--------------------+-----------+----+------------+-------+----------------------+---------------------+

To view the state of a specific job, use the --name=NAME option, where NAME can be the
job id or the job name ::

    $ cm hpc queue --name=6
    +---------+-------+-----------+-------------+-----------+----+------+-------+----------+---------------------+
    | cluster | jobid | partition | name        | user      | st | time | nodes | nodelist | updated             |
    +---------+-------+-----------+-------------+-----------+----+------+-------+----------+---------------------+
    | india   | 6     | xxxxx     | somethin.sh | xxxxxxxxx | PD | 0:00 | 1     |          | 2015-11-29 16:24:15 |
    +---------+-------+-----------+-------------+-----------+----+------+-------+----------+---------------------+

