<?php
class Shooting
{
    private string $f1;
    private string $f2;
    private float $x0;
    private array $nu;
    private float $a0;
    private float $b0;
    private float $a1;
    private float $b1;
    private float $A;
    private float $B;
    private float $a;
    private float $b;
    private int $e;

    private function func1($nu, $a1, $b1, $B)
    {
        $q = $this->Euler($nu);
        return $a1 * $q[0] + $b1 * $q[1] - $B;
    }

    private function func($f, $x, $y, $z)
    {
        $f = str_replace("x", $x, $f);
        $f = str_replace("y", $y, $f);
        $f = str_replace("z", $z, $f);
        $f = str_replace("--", "+", $f);
        $f = str_replace("++", "+", $f);
        $f = str_replace("+-", "-", $f);
        $p = eval('return ' . $f . ';');
        return $p;
    }
    private function num($nu2, $nu1)
    {
        $obj1 =  $this->func1($nu1, $this->a1, $this->b1, $this->B);
        $obj2 =  $this->func1($nu2, $this->a1, $this->b1, $this->B);
        return $nu2 - (($obj2 * ($nu2 - $nu1)) / ($obj2 - $obj1));
    }

    public function __construct(string $f1, string $f2, float $x0, array $nu, float $a0, float $b0, float $a1, float $b1, float $A, float $B, float $a, float $b, int $e = 2)
    {
        $this->f1 = $f1;
        $this->f2 = $f2;
        $this->x0 = $x0;
        $this->nu = $nu;
        $this->a0 = $a0;
        $this->b0 = $b0;
        $this->a1 = $a1;
        $this->b1 = $b1;
        $this->A = $A;
        $this->B = $B;
        $this->a = $a;
        $this->b = $b;
        $this->e = $e;
    }

    public function Euler($nu)
    {
        $m = abs($this->b - $this->a) * 10 ** $this->e;
        $h = 1 * (10 ** -$this->e);

        $x = array($this->x0);
        if ($this->b0 == 0) {
            $y = array($this->A / $this->a0);
            $z = array($nu);
        } elseif ($this->b0 != 0) {
            $y = array($nu);
            $z = array(($this->A - $this->a0 * $nu) / $this->b0);
        }

        for ($i = 1; $i < $m + 1; $i++) {
            $x[$i] = $this->x0 + $h * $i;
            $y[$i] = $y[$i - 1] + $h * $this->func($this->f1, $x[$i - 1], $y[$i - 1], $z[$i - 1]);
            $z[$i] = $z[$i - 1] + $h * $this->func($this->f2, $x[$i - 1], $y[$i - 1], $z[$i - 1]);
        }
        return array($y[$m], $z[$m]);
    }
    public function Start()
    {
        $i = 1;
        do {
            $o = $this->num($this->nu[$i], $this->nu[$i - 1]);
            $nu[$i + 1] = $o;
            ++$i;
        } while ($nu[$i] == $nu[$i - 1]);
        return $o;
    }
    public function Requirement()
    {
        $o = $this->Start();
        return sprintf("y\' = %s\nz\' = %s\ny(%h) = %f\ny'(%h) = %f\n", $this->f1, $this->f2, $this->a, $this->A, $this->a, $o);
    }
}

function Main()
{
    $f1 = "z";
    $f2 = "-x - y";
    $x0 = 0;
    $nu = array(1, -1);
    $a0 = 1;
    $b0 = 0;
    $a1 = 1;
    $b1 = 0;
    $A = 0;
    $B = 0;
    $a = 0;
    $b = 1;

    $obj = new Shooting($f1, $f2, $x0, $nu, $a0, $b0, $a1, $b1, $A, $B, $a, $b);
    $y = $obj->Requirement();
    echo $y;
}

Main();

?>